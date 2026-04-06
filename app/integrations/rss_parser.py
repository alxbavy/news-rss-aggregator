from __future__ import annotations

from calendar import timegm
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import logging
from urllib.parse import urldefrag, urlparse
import uuid

import feedparser

from app.models.feed_source import FeedSource


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ParsedPost:
    source_id: uuid.UUID
    title: str
    link: str
    published_at: datetime | None
    content_hash: str


class RSSParser:
    USER_AGENT = "news-rss-aggregator/1.0"

    def parse(self, source: FeedSource) -> list[ParsedPost]:
        logger.info("Parsing feed '%s' (%s)", source.name, source.url)

        parsed_feed = feedparser.parse(
            str(source.url),
            request_headers={
                "User-Agent": self.USER_AGENT,
                "Accept": (
                    "application/atom+xml, application/rss+xml, "
                    "application/xml, text/xml;q=0.9, */*;q=0.8"
                ),
            },
        )

        if getattr(parsed_feed, "bozo", False):
            logger.warning(
                "Feed '%s' parsed with warnings",
                source.url,
                exc_info=getattr(parsed_feed, "bozo_exception", None),
            )

        posts: list[ParsedPost] = []
        seen_hashes: set[str] = set()

        for entry in getattr(parsed_feed, "entries", []) or []:
            title = self._extract_title(entry)
            link = self._extract_link(entry)

            if not title or not link:
                logger.debug("Skipping feed entry without title or link: %s", entry)
                continue

            published_at = self._extract_published_at(entry)
            stable_key = self._extract_stable_key(
                entry=entry,
                link=link,
                title=title,
                published_at=published_at,
            )
            content_hash = self._build_content_hash(stable_key)

            if content_hash in seen_hashes:
                continue

            seen_hashes.add(content_hash)
            posts.append(
                ParsedPost(
                    source_id=source.id,
                    title=title,
                    link=link,
                    published_at=published_at,
                    content_hash=content_hash,
                )
            )

        logger.info(
            "Parsed %s entries from feed '%s'",
            len(posts),
            source.url,
        )
        return posts

    @staticmethod
    def _extract_title(entry) -> str:
        return RSSParser._pick_text(
            getattr(entry, "title", None),
            getattr(getattr(entry, "title_detail", None), "value", None),
            getattr(entry, "summary", None),
        )

    @staticmethod
    def _extract_link(entry) -> str:
        for link_info in getattr(entry, "links", []) or []:
            href = RSSParser._pick_text(link_info.get("href"))
            rel = RSSParser._pick_text(link_info.get("rel")).lower()

            if href and rel in {"alternate", "related", ""} and RSSParser._is_article_url(href):
                return RSSParser._normalize_url(href)

        direct_link = RSSParser._pick_text(getattr(entry, "link", None))
        if direct_link and RSSParser._is_article_url(direct_link):
            return RSSParser._normalize_url(direct_link)

        return ""

    @staticmethod
    def _is_article_url(value: str) -> bool:
        parsed = urlparse(value.strip())
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

    @staticmethod
    def _extract_published_at(entry) -> datetime | None:
        time_struct = (
            getattr(entry, "published_parsed", None)
            or getattr(entry, "updated_parsed", None)
        )
        if time_struct is None:
            return None

        try:
            return datetime.fromtimestamp(timegm(time_struct), tz=timezone.utc)
        except (OverflowError, TypeError, ValueError):
            logger.warning("Failed to convert published date for entry: %s", entry)
            return None

    @staticmethod
    def _extract_stable_key(
        entry,
        link: str,
        title: str,
        published_at: datetime | None,
    ) -> str:
        opaque_id = RSSParser._pick_text(
            getattr(entry, "id", None),
            getattr(entry, "guid", None),
        )
        if opaque_id:
            return opaque_id

        if link:
            return link

        published_part = published_at.isoformat() if published_at else ""
        return f"{title}|{published_part}"

    @staticmethod
    def _build_content_hash(stable_key: str) -> str:
        return sha256(stable_key.encode("utf-8")).hexdigest()

    @staticmethod
    def _normalize_url(url: str) -> str:
        normalized, _fragment = urldefrag(url.strip())
        return normalized

    @staticmethod
    def _pick_text(*values: object) -> str:
        for value in values:
            if value is None:
                continue

            text = str(value).strip()
            if text:
                return " ".join(text.split())

        return ""
