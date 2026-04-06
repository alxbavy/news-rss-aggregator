from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.storage import Storage

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def admin_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/index.html",
        context={},
    )


@router.get("/feed-sources", response_class=HTMLResponse)
def feed_sources_list(request: Request, db: Session = Depends(get_db)):
    storage = Storage(session=db)
    items = storage.get_all_feed_sources()

    return templates.TemplateResponse(
        request=request,
        name="admin/feed_sources/list.html",
        context={"items": items},
    )


@router.get("/feed-sources/create", response_class=HTMLResponse)
def feed_sources_create_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/feed_sources/create.html",
        context={},
    )


@router.get("/telegram-chats", response_class=HTMLResponse)
def telegram_chats_list(request: Request, db: Session = Depends(get_db)):
    storage = Storage(session=db)
    items = storage.get_all_telegram_chats()

    return templates.TemplateResponse(
        request=request,
        name="admin/telegram_chats/list.html",
        context={"items": items},
    )


@router.get("/telegram-chats/create", response_class=HTMLResponse)
def telegram_chats_create_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/telegram_chats/create.html",
        context={},
    )
