from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import uuid

import pytest

from app.integrations.rss_parser import RSSParser


FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "rss"


@dataclass(slots=True)
class FakeFeedSource:
    id: uuid.UUID
    name: str
    url: str


def build_source(fixture_name: str) -> FakeFeedSource:
    fixture_path = (FIXTURES_DIR / fixture_name).resolve()

    return FakeFeedSource(
        id=uuid.uuid4(),
        name=fixture_path.stem,
        url=fixture_path.as_uri(),
    )


@pytest.fixture
def parser() -> RSSParser:
    return RSSParser()


def test_parse__rss20_feed_with_pubdate__returns_posts_with_expected_fields(
    parser: RSSParser,
) -> None:
    source = build_source("bbc_like_rss.xml")

    posts = parser.parse(source)

    assert len(posts) == 2

    first = posts[0]
    assert first.source_id == source.id
    assert first.title == "BBC-like story one"
    assert first.link == "https://news.example.com/world/story-1"
    assert first.published_at == datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc)
    assert len(first.content_hash) == 64

    second = posts[1]
    assert second.title == "BBC-like story two"
    assert second.link == "https://news.example.com/world/story-2"
    assert second.published_at == datetime(2026, 4, 6, 10, 0, tzinfo=timezone.utc)


def test_parse__atom_feed_with_alternate_link_and_updated__returns_normalized_posts(
    parser: RSSParser,
) -> None:
    source = build_source("guardian_like_atom.xml")

    posts = parser.parse(source)

    assert len(posts) == 2

    first = posts[0]
    assert first.title == "Guardian-like entry one"
    assert first.link == "https://news.example.com/politics/entry-1"
    assert first.published_at == datetime(2026, 4, 6, 11, 15, tzinfo=timezone.utc)

    second = posts[1]
    assert second.title == "Guardian-like entry two"
    assert second.link == "https://news.example.com/politics/entry-2"
    assert second.published_at == datetime(2026, 4, 6, 11, 45, tzinfo=timezone.utc)


def test_parse__feed_without_pubdate__returns_post_with_none_published_at(
    parser: RSSParser,
) -> None:
    source = build_source("sky_like_rss_no_pubdate.xml")

    posts = parser.parse(source)

    assert len(posts) == 1
    assert posts[0].title == "Sky-like story without publication date"
    assert posts[0].link == "https://news.example.com/uk/story-without-date"
    assert posts[0].published_at is None
    assert len(posts[0].content_hash) == 64


def test_parse__feed_with_duplicate_guid__deduplicates_posts(
    parser: RSSParser,
) -> None:
    source = build_source("abc_like_rss_duplicates.xml")

    posts = parser.parse(source)

    assert len(posts) == 2
    assert [post.title for post in posts] == [
        "Duplicate candidate story",
        "Unique story",
    ]
    assert [post.link for post in posts] == [
        "https://news.example.com/world/duplicate-story",
        "https://news.example.com/world/unique-story",
    ]


def test_parse__feed_with_invalid_entries_and_link_fragment__skips_invalid_and_strips_fragment(
    parser: RSSParser,
) -> None:
    source = build_source("dw_like_atom_invalid_entries.xml")

    posts = parser.parse(source)

    assert len(posts) == 1

    post = posts[0]
    assert post.title == "Valid entry with fragment in link"
    assert post.link == "https://news.example.com/europe/valid-entry"
    assert post.published_at == datetime(2026, 4, 6, 12, 30, tzinfo=timezone.utc)