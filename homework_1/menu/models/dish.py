import uuid

from sqlalchemy import Column, String, Float, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from core.orm import Base


class DishModel(Base):
    '''Модель для описания таблицы с данными блюда'''
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=255), nullable=False)
    price = Column(Float, nullable=False)
    submenu_id = Column(UUID(as_uuid=True), default=uuid.uuid4)

    submenu = relationship('SubmenuModel', back_populates='dishes', uselist=False)

    __tablename__ = 'dish'
    __table_args__ = (
        ForeignKeyConstraint(
            ['submenu_id'],
            ['submenu.id'],
            name='dish__submenu_id__fk',
            ondelete='CASCADE',
        ),
        UniqueConstraint(
            name,
            name='dish__name__uniq'
        )
    )
