import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TelegramChatBase(BaseModel):
    chat_id: int
    title: str | None = None
    is_active: bool = True


class TelegramChatCreate(TelegramChatBase):
    pass


class TelegramChatUpdate(BaseModel):
    title: str | None = None
    is_active: bool | None = None


class TelegramChatRead(TelegramChatBase):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
