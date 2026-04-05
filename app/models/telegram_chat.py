import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Uuid, func, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TelegramChat(Base):
    __tablename__ = "telegram_chats"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    chat_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        unique=True,
    )
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
