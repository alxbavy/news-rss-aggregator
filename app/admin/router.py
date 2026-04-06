from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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
def feed_sources_list(request: Request):
    items = []
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
def telegram_chats_list(request: Request):
    items = []
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
