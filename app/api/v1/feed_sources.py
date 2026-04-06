from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.storage import Storage
from app.schemas.feed_source import FeedSourceCreate, FeedSourceRead


router = APIRouter(prefix="/feed-sources", tags=["feed-sources"])


@router.post("", response_model=FeedSourceRead, status_code=201)
def create_feed_source(
    payload: FeedSourceCreate,
    db: Session = Depends(get_db),
) -> FeedSourceRead:
    storage = Storage(session=db)
    return storage.create_feed_source(payload)


@router.get("", response_model=list[FeedSourceRead])
def list_feed_sources(
    db: Session = Depends(get_db),
) -> list[FeedSourceRead]:
    storage = Storage(session=db)
    return storage.get_all_feed_sources()
