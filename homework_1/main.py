from fastapi import FastAPI

from core.settings.settings import settings
from menu.routers.routers import router

app = FastAPI(title=settings.app.project_name)

app.include_router(router)
