from pydantic import PostgresDsn, validator

from core.settings.base import CommonSettings


class DBSettings(CommonSettings):
    '''Настройки БД'''
    name: str
    user: str
    password: str
    host: str
    port: int
    url: PostgresDsn | None = None

    @validator('url', pre=True, always=True)
    def make_db_connection_url(cls, value, values):
        '''Сделать урл для подключения к БД'''
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('user'),
            password=values.get('password'),
            host=values.get('host'),
            port=str(values.get('port')),
            path=f'/{values.get("name") or ""}',
        )
