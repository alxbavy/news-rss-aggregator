from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import logging
import uuid

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
    def parse(self, source: FeedSource) -> list[ParsedPost]:
        pass
