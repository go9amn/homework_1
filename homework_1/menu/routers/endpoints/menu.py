from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from core.orm import create_db_session
from core.repositories.base import Repository
from core.repositories.enums import SQLOperators
from menu.models.dish import DishModel
from menu.models.menu import MenuModel
from menu.models.submenu import SubmenuModel
from menu.schemas.menu import MenuCreateSchema, MenuReadSchema, MenuUpdateSchema


router = APIRouter()


@router.post(
    '',
    response_model=MenuReadSchema,
    description='Эндопоинт для создания меню'
)
async def create_menu(
    request_body: MenuCreateSchema,
    db_session: AsyncSession = Depends(create_db_session),
) -> MenuModel:
    repository = Repository(db_session)
    menu = repository.add_obj_to_session(model=MenuModel, data=request_body.dict())
    await repository.commit()

    return menu


@router.get(
    '/{menu_id}',
    response_model=MenuReadSchema,
    description='Эндпоинт для получения данных меню'
)
async def get_menu(
    menu_id: UUID,
    db_session: AsyncSession = Depends(create_db_session),
) -> MenuModel:
    repository = Repository(db_session)
    menu = await repository.select_one(
        model=MenuModel,
        conditions=(
            ('id', SQLOperators.EQ, menu_id),
        ),
    )
    submenus = await repository.select_list(
        model=SubmenuModel,
        conditions=(
            ('menu_id', SQLOperators.EQ, menu_id),
        ),
    )

    list_id = [item.id for item in submenus]
    menu.submenus_amount = len(list_id)

    dishes_amount = 0
    for submenu_id in list_id:
        dishes_amount += len(await repository.select_list(
            model=DishModel,
            conditions=(
                ('submenu_id', SQLOperators.EQ, submenu_id),
            ),
        ))
    menu.dishes_amount = dishes_amount

    return menu


@router.patch(
    '/{menu_id}',
    response_model=MenuReadSchema,
    description='Эндпоинт для обновления данных меню',
)
async def update_menu(
    menu_id: UUID,
    request_body: MenuUpdateSchema,
    db_session: AsyncSession = Depends(create_db_session),
) -> MenuModel:
    repository = Repository(db_session)
    menu = await repository.update_and_return_one(
        model=MenuModel,
        data=request_body.dict(exclude_unset=True),
        conditions=(
            ('id', SQLOperators.EQ, menu_id),
        ),
    )
    await repository.commit()

    return menu


@router.delete(
    '/{menu_id}',
    description='Эндопоинт для удаления меню',
)
async def delete_menu(
    menu_id: UUID,
    db_session: AsyncSession = Depends(create_db_session),
) -> None:
    repository = Repository(db_session)
    await repository.delete(model=MenuModel, conditions=(('id', SQLOperators.EQ, menu_id),),)
    await repository.commit()
