import uuid

from sqlalchemy import Column, String, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.orm import Base


class SubmenuModel(Base):
    '''Модель для описания таблицы с данными подменю'''
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    menu_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    name = Column(String(length=255), nullable=False)

    dishes = relationship('DishModel', back_populates='submenu')

    __tablename__ = 'submenu'
    __table_args__ = (
        ForeignKeyConstraint(
            ['menu_id'],
            ['menu.id'],
            name='submenu__menu_id__fk',
            ondelete='CASCADE',
        ),
        UniqueConstraint(
            name,
            name='submenu__name__uniq',
        )
    )
