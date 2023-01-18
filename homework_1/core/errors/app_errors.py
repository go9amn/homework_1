from fastapi import status

from core.errors.base import BaseAppError
from core.errors.error_codes import AppErrorCode


class ResourceNotFoundError(BaseAppError):
    '''Не найден запрашиваемый ресурс -- запись в БД и тд'''
    _http_status_code = status.HTTP_404_NOT_FOUND
    _message: str = 'Запрашиваемый ресурс не найден'
    _code: AppErrorCode = AppErrorCode.RESOURCENOTFOUND


class ResourceConflictError(BaseAppError):
    '''Конфликт при создании или обновлении ресурса'''
    _http_status_code = status.HTTP_409_CONFLICT
    _message: str = 'Возник конфликт при попытке выполнить запрос'
    _code: AppErrorCode = AppErrorCode.RESOURCECONFLICT
