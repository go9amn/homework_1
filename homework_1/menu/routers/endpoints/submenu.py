from fastapi import APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from core.orm import create_db_session
from core.repositories.base import Repository
from core.repositories.enums import SQLOperators
from menu.models.submenu import SubmenuModel
from menu.models.dish import DishModel
from menu.schemas.submenu import SubmenuCreateSchema, SubmenuReadSchema, SubmenuUpdateSchema


router = APIRouter()


@router.post(
    '/{menu_id}/submenus',
    response_model=SubmenuReadSchema,
    description='Эндопнит для создания подменю',
)
async def create_submenu(
    request_body: SubmenuCreateSchema,
    menu_id: UUID,
    db_session: AsyncSession = Depends(create_db_session),
) -> SubmenuModel:
    repository = Repository(db_session)
    submenu = repository.add_obj_to_session(
        model=SubmenuModel,
        data={**request_body.dict(), 'menu_id': menu_id}
    )
    await repository.commit()

    return submenu


@router.get(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=SubmenuReadSchema,
    description='Эндпоинт для получения данных подменю',
)
async def get_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    db_session: AsyncSession = Depends(create_db_session),
) -> SubmenuModel:
    repository = Repository(db_session)
    submenu = await repository.select_one(
        model=SubmenuModel,
        conditions=(
            ('id', SQLOperators.EQ, submenu_id),
        ),
    )

    amount_of_dishes = await repository.select_list(
        model=DishModel,
        conditions=(
            ('submenu_id', SQLOperators.EQ, submenu_id),
        ),
    )

    submenu.amount_of_dishes = len(amount_of_dishes)

    return submenu


@router.patch(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=SubmenuReadSchema,
    description='Эндпоинт для обновления данных подменю',
)
async def update_submenus(
    menu_id: UUID,
    submenu_id: UUID,
    request_body: SubmenuUpdateSchema,
    db_session: AsyncSession = Depends(create_db_session),
) -> SubmenuModel:
    repository = Repository(db_session)
    submenu = await repository.update_and_return_one(
        model=SubmenuModel,
        data=request_body.dict(),
        conditions=(
            ('id', SQLOperators.EQ, submenu_id),
        ),
    )
    await repository.commit()

    return submenu


@router.delete(
    '/{menu_id}/submenus/{submenu_id}',
    description='Эндпоинт для удаления данных подменю'
)
async def delete_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    db_session: AsyncSession = Depends(create_db_session),
) -> None:
    repository = Repository(db_session)
    await repository.delete(
        model=SubmenuModel,
        conditions=(
            ('id', SQLOperators.EQ, submenu_id),
        ),
    )
    await repository.commit()
