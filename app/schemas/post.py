import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class PostBase(BaseModel):
    title: str
    link: HttpUrl
    published_at: datetime | None = None


class PostCreate(PostBase):
    source_id: uuid.UUID


class PostRead(PostBase):
    id: uuid.UUID
    source_id: uuid.UUID
    notified_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
