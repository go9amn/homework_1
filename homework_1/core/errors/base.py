from typing import Any

from core.errors.error_codes import AppErrorCode, SystemErrorCode


class BaseAppError(Exception):
    '''Базовый класс ошибок приложения.
    Не делай raise этого исключения, посмотри в app_errors.py,
    если там нет подходящего -- заведи новый подкласс
    '''

    _http_status_code = None  # type: int
    _code = None  # type: [AppErrorCode, SystemErrorCode]
    _message = None  # type: str

    def __init__(
        self,
        user_error_message: str | None = None,
        *,
        system_error_message: str | None = None,
        details: dict[Any, Any] | None = None,
        headers: dict[str, Any] | None = None,
        http_status_code: int | None = None
    ):
        super().__init__()
        self.code = self._code
        self.http_status_code = http_status_code or self._http_status_code
        self.user_error = user_error_message or self._message
        self.system_error = system_error_message
        self.headers = headers
        self.details: dict = details if isinstance(details, dict) else {'error': details}

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return (
            f'{class_name}'
            f'(user_error_message={self.user_error!r},'
            f'system_error_message={self.system_error!r},'
            f'details={self.details!r},'
            f'headers={self.headers!r}),'
            f'http_status_code={self.http_status_code!r})'
        )

    def __str__(self) -> str:
        return repr(self)
