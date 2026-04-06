import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.feed_source import FeedSource
from app.models.post import Post
from app.models.telegram_chat import TelegramChat
from app.schemas.feed_source import FeedSourceRead, FeedSourceCreate
from app.schemas.post import PostCreate, PostRead
from app.schemas.telegram_chat import TelegramChatRead, TelegramChatCreate


class Storage:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all_feed_sources(self) -> list[FeedSourceRead]:
        items = self.session.query(FeedSource).all()
        return [FeedSourceRead.model_validate(item) for item in items]

    def create_feed_source(self, payload: FeedSourceCreate) -> FeedSourceRead:
        item = FeedSource(
            name=payload.name,
            url=str(payload.url),
            is_active=payload.is_active,
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return FeedSourceRead.model_validate(item)

    def get_all_telegram_chats(self) -> list[TelegramChatRead]:
        items = self.session.query(TelegramChat).all()
        return [TelegramChatRead.model_validate(item) for item in items]

    def create_telegram_chat(self, payload: TelegramChatCreate) -> TelegramChatRead:
        item = TelegramChat(
            chat_id=payload.chat_id,
            title=payload.title,
            is_active=payload.is_active,
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return TelegramChatRead.model_validate(item)
