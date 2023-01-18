from pydantic import Field

from core.settings.base import CommonSettings


class AppSettings(CommonSettings):
    '''Настройки для всего приложения'''
    project_name: str = Field('MenuApp', description='Название проекта')
    api_v1_str: str = Field(
        '/v1',
        description='Строка с номером 1й версии API для добавления к эндпоинтам 1й версии',
    )
