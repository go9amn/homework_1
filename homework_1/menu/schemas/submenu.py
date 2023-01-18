from pydantic import BaseModel, Field
from uuid import UUID

from menu.models.submenu import SubmenuModel


class SubmenuBaseSchema(BaseModel):
    '''Базовая схема данных подменю'''
    name: str = Field(
        description='Название подменю',
        min_length=1,
        max_length=255,
    )

    class Config:
        orm_mode = True
        orig_model = SubmenuModel


class SubmenuCreateSchema(SubmenuBaseSchema):
    '''Схема данных подменю при его создании'''
    pass


class SubmenuReadSchema(SubmenuBaseSchema):
    '''Схема данных подменю при получении данных'''
    id: UUID
    amount_of_dishes: int = 0


class SubmenuUpdateSchema(SubmenuBaseSchema):
    '''Схема данных подменю при обновлении данных'''
    name: str | None = Field(
        description='Название подменю',
        min_length=1,
        max_length=255,
    )
