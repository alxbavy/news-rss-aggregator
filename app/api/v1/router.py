from fastapi import APIRouter


from app.api.v1.feed_sources import router as feed_sources_router
from app.api.v1.health import router as health_router
from app.api.v1.telegram_chats import router as telegram_chats_router


api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(feed_sources_router)
api_router.include_router(telegram_chats_router)
