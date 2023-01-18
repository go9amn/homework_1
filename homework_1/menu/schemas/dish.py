from pydantic import BaseModel, Field, ValidationError, validator
from uuid import UUID

from menu.models.dish import DishModel


class DishBaseSchema(BaseModel):
    '''Базовая схема данных блюда'''
    name: str = Field(
        description='Название блюда',
        min_length=1,
        max_length=255,
    )

    price: float = Field(
        description='Цена блюда',
        gt=0,
        lt=1000000,
    )

    class Config:
        orm_mode = True
        orig_model = DishModel


class DishCreateSchema(DishBaseSchema):
    '''Схема данных блюда при его создании'''
    pass


class DishReadSchema(DishBaseSchema):
    '''Схема данных блюда при получении данных'''
    id: UUID

    @validator('price')
    def round_to_two(cls, price):
        return round(price, 2)


class DishUpdateSchema(DishBaseSchema):
    '''Схема данных для обновления данных блюда'''
    name: str | None = Field(
        description='Название блюда',
        min_length=1,
        max_length=255,
    )

    price: float | None = Field(
        description='Цена блюда',
        gt=0,
        lt=1000000,
    )
