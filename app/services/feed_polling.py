from __future__ import annotations

import logging

from app.integrations.rss_parser import RSSParser
from app.integrations.telegram_notifier import TelegramNotifier
from app.repositories.storage import Storage
from app.schemas.feed_polling import FeedPollingResult
from app.schemas.post import PostCreate

logger = logging.getLogger(__name__)


class FeedPollingService:
    def __init__(self, parser, storage, notifier) -> None:
        self.parser: RSSParser = parser
        self.storage: Storage = storage
        self.notifier: TelegramNotifier = notifier

    def check_new_posts(self) -> FeedPollingResult:
        result = FeedPollingResult()

        sources = self.storage.get_active_sources()
        chats = self.storage.get_active_chats()

        for source in sources:
            try:
                parsed_posts = self.parser.parse(source)
            except Exception:
                logger.exception(
                    "Failed to parse source '%s' (%s)",
                    source.name,
                    source.url,
                )
                continue

            for item in parsed_posts:
                existing = self.storage.get_post_by_hash(
                    source_id=item.source_id,
                    content_hash=item.content_hash,
                )
                if existing is not None:
                    continue

                created_post = self.storage.create_post(
                    PostCreate(
                        source_id=item.source_id,
                        title=item.title,
                        link=item.link,
                        published_at=item.published_at,
                        content_hash=item.content_hash,
                    )
                )

                for chat in chats:
                    try:
                        self.notifier.send_post_notification(
                            chat_id=chat.chat_id,
                            title=created_post.title,
                            link=str(created_post.link),
                        )
                    except Exception:
                        logger.exception(
                            "Failed to notify chat_id=%s about post_id=%s",
                            chat.chat_id,
                            created_post.id,
                        )

                self.storage.mark_as_notified(created_post.id)

        return result
