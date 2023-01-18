import enum


@enum.unique
class SystemErrorCode(str, enum.Enum):

    SCHEMAVIOLATED = 'SCHEMAVIOLATED'
    INTERNAL = 'INTERNAL'
    METHODNOTALLOWED = 'NOTALLOWED'
    NOTFOUND = 'NOTFOUND'
    UNKNOWN = 'UNKNOWN'


@enum.unique
class AppErrorCode(str, enum.Enum):
    '''Ошибки бизнес логики приложения.'''

    BADREQUEST = 'BADREQUEST'
    FORBIDDEN = 'FORBIDDEN'
    RESOURCECONFLICT = 'RESOURCECONFLICT'
    RESOURCENOTFOUND = 'RESOURCENOTFOUND'
    UNAUTHORIZED = 'UNAUTHORIZED'
