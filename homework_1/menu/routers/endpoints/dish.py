from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from core.orm import create_db_session
from core.repositories.base import Repository
from core.repositories.enums import SQLOperators
from menu.models.dish import DishModel
from menu.schemas.dish import DishCreateSchema, DishReadSchema, DishUpdateSchema


router = APIRouter()


@router.post(
    '/{submenu_id}/dishes',
    response_model=DishReadSchema,
    description='Эндопнит для создания блюда',
)
async def create_dish(
    submenu_id: UUID,
    request_body: DishCreateSchema,
    db_session: AsyncSession = Depends(create_db_session),
) -> DishModel:
    repository = Repository(db_session)
    dish = repository.add_obj_to_session(
        model=DishModel,
        data={**request_body.dict(), 'submenu_id': submenu_id},
    )
    await repository.commit()

    return dish


@router.get(
    '/{submenu_id}/dishes/{dish_id}',
    response_model=DishReadSchema,
    description='Эндпоинта для получения данных блюда',
)
async def read_dish(
    dish_id: UUID,
    submenu_id: UUID,
    db_session: AsyncSession = Depends(create_db_session),
) -> DishModel:
    repository = Repository(db_session)
    dish = await repository.select_one(
        model=DishModel,
        conditions=(
            ('id', SQLOperators.EQ, dish_id),
        ),
    )

    return dish


@router.patch(
    '/{submenu_id}/dishes/{dish_id}',
    response_model=DishReadSchema,
    description='Эндпоинта для обновления данных блюда',
)
async def update_dish(
    dish_id: UUID,
    submenu_id: UUID,
    response_body: DishUpdateSchema,
    db_session: AsyncSession = Depends(create_db_session),
) -> DishModel:
    repository = Repository(db_session)
    dish = await repository.update_and_return_one(
        model=DishModel,
        data=response_body.dict(exclude_unset=True),
        conditions=(
            ('id', SQLOperators.EQ, dish_id),
        ),
    )
    await repository.commit()

    return dish


@router.delete(
    '/{submenu_id}/dishes/{dish_id}',
    description='Эндпоинта для удаления блюда',
)
async def delete_dish(
    dish_id: UUID,
    submenu_id: UUID,
    db_session: AsyncSession = Depends(create_db_session),
) -> None:
    repository = Repository(db_session)
    await repository.delete(
        model=DishModel,
        conditions=(
            ('id', SQLOperators.EQ, dish_id),
        ),
    )
    await repository.commit()
