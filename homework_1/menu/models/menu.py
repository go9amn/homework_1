import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from core.orm import Base


class MenuModel(Base):
    '''Модель для описания таблицы с данными меню'''
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=255), nullable=False)

    __tablename__ = 'menu'
