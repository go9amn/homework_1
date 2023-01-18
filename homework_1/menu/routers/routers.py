from fastapi import APIRouter

from core.settings.settings import settings
from menu.routers.endpoints import dish
from menu.routers.endpoints import menu
from menu.routers.endpoints import submenu


router = APIRouter()

router.include_router(
    menu.router,
    prefix=f'{settings.app.api_v1_str}/menus',
    tags=['Меню'],
)

router.include_router(
    submenu.router,
    prefix=f'{settings.app.api_v1_str}/menus',
    tags=['Подменю']
)

router.include_router(
    dish.router,
    prefix=f'{settings.app.api_v1_str}/submenus',
    tags=['Блюда'],
)
