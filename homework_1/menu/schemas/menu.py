from pydantic import BaseModel, Field
from uuid import UUID

from menu.models.menu import MenuModel


class MenuBaseSchema(BaseModel):
    '''Базовая схема данных меню'''
    name: str = Field(
        description='Название блюда',
        min_length=1,
        max_length=255,
    )

    class Config:
        orm_mode = True
        orig_model = MenuModel


class MenuCreateSchema(MenuBaseSchema):
    '''Схема данных меню при его создании'''
    pass


class MenuReadSchema(MenuBaseSchema):
    '''Схема данных меню при получении данных'''
    id: UUID
    submenus_amount: int = 0
    dishes_amount: int = 0


class MenuUpdateSchema(MenuBaseSchema):
    '''Схема данных меню при обновлении данных'''
    name: str | None = Field(
        description='Название блюда',
        min_length=1,
        max_length=255,
    )
