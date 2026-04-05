import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class FeedSourceBase(BaseModel):
    name: str
    url: HttpUrl
    is_active: bool = True


class FeedSourceCreate(FeedSourceBase):
    pass


class FeedSourceUpdate(BaseModel):
    name: str | None = None
    url: HttpUrl | None = None
    is_active: bool | None = None


class FeedSourceRead(FeedSourceBase):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
