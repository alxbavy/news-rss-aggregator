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

    def get_active_sources(self) -> list[FeedSource]:
        return (
            self.session.query(FeedSource)
            .filter(FeedSource.is_active.is_(True))
            .all()
        )

    def get_active_chats(self) -> list[TelegramChat]:
        return (
            self.session.query(TelegramChat)
            .filter(TelegramChat.is_active.is_(True))
            .all()
        )

    def get_post_by_hash(self, source_id: uuid.UUID, content_hash: str) -> Post | None:
        return (
            self.session.query(Post)
            .filter(
                Post.source_id == source_id,
                Post.content_hash == content_hash,
            )
            .first()
        )

    def create_post(self, payload: PostCreate) -> PostRead:
        item = Post(
            source_id=payload.source_id,
            title=payload.title,
            link=str(payload.link),
            published_at=payload.published_at,
            content_hash=payload.content_hash,
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return PostRead.model_validate(item)

    def mark_as_notified(self, post_id: uuid.UUID) -> None:
        post = self.session.get(Post, post_id)
        if post is None:
            return

        post.notified_at = datetime.now(timezone.utc)
        self.session.commit()
