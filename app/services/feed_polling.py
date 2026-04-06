from __future__ import annotations

import logging

from app.schemas.feed_polling import FeedPollingResult

logger = logging.getLogger(__name__)


class FeedPollingService:
    def __init__(self, parser, storage, notifier) -> None:
        self.parser = parser
        # self.storage = storage # TODO
        self.notifier = notifier

    def check_new_posts(self) -> FeedPollingResult:
        pass
