from pydantic import BaseSettings

from core.settings.app import AppSettings
from core.settings.db import DBSettings


class Settings(BaseSettings):
    '''Класс с настройками и переменными всего проекта'''
    app: AppSettings = AppSettings()
    db: DBSettings

    class Config:
        allow_mutation = False
        env_nested_delimiter = '__'
        env_file = '.env'


settings = Settings()
