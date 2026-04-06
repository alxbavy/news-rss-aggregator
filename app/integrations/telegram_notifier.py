from __future__ import annotations

import asyncio
from html import escape
import logging

from aiogram import Bot
from aiogram.enums import ParseMode


logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, bot_token: str) -> None:
        self._bot_token = bot_token

    def send_post_notification(self, chat_id: int, title: str, link: str) -> None:
        asyncio.run(
            self._send_post_notification(
                chat_id=chat_id,
                title=title,
                link=link,
            )
        )

    async def _send_post_notification(self, chat_id: int, title: str, link: str) -> None:
        message_text = self._build_message(title=title, link=link)

        async with Bot(self._bot_token).context() as bot:
            await bot.send_message(
                chat_id=chat_id,
                text=message_text,
                parse_mode=ParseMode.HTML,
            )

        logger.info("Telegram notification sent to chat_id=%s", chat_id)

    @staticmethod
    def _build_message(title: str, link: str) -> str:
        safe_title = escape(title)
        safe_link = escape(link)
        return f"<b>{safe_title}</b>\n{safe_link}"
