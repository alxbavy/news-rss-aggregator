from fastapi import FastAPI

from app.api.v1.router import api_router
from app.admin.router import router as admin_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(api_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/admin", tags=["admin"])
