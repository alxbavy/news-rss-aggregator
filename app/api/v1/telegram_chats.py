from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.storage import Storage
from app.schemas.telegram_chat import TelegramChatCreate, TelegramChatRead


router = APIRouter(prefix="/telegram-chats", tags=["telegram-chats"])


@router.post("", response_model=TelegramChatRead, status_code=201)
def create_telegram_chat(
    payload: TelegramChatCreate,
    db: Session = Depends(get_db),
) -> TelegramChatRead:
    storage = Storage(session=db)
    return storage.create_telegram_chat(payload)


@router.get("", response_model=list[TelegramChatRead])
def list_telegram_chats(
    db: Session = Depends(get_db),
) -> list[TelegramChatRead]:
    storage = Storage(session=db)
    return storage.get_all_telegram_chats()
