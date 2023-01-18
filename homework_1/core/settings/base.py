from pydantic import BaseModel


class CommonSettings(BaseModel):
    '''Общие параметры для всех классов settings,
    которые выступают, как поля в базовом классе
    настроек

    '''

    class Config:
        allow_mutation = False
