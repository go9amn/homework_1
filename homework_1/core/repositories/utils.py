from functools import wraps
from typing import Callable, TypeVar

from core.orm import Base


Model = TypeVar('Model', bound=Base)


def convert_sqlalchemy_row_to_model(repo_method: Callable) -> Callable:
    '''Преобразовать sqlalchemy.engine.row.Row объект
    в экземпляр соответсвующей модели

    '''
    @wraps(repo_method)
    async def wrapper(*args, **kwargs) -> Model:
        sqlalchemy_row = await repo_method(*args, **kwargs)

        return kwargs['model'](**sqlalchemy_row._asdict())

    return wrapper
