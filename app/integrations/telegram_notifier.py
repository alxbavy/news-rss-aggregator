from __future__ import annotations

import logging


logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, bot_token: str) -> None:
        self._bot_token = bot_token

    def send_post_notification(self, chat_id: int, title: str, link: str) -> None:
        pass
