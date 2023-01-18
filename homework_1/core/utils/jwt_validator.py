from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import exceptions as jwt_exceptions, jwt

from core.errors.app_errors import UnauthorizedError
from core.settings.settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class JWTValidator:
    '''Сервис для валидации JWT токенов'''
    def validate_access_token(self, access_token: str = Depends(oauth2_scheme)) -> str:
        '''Проверить валидность access token'''
        user_id = self._validate_token(access_token, settings.jwt.access_token_secret_key)

        return user_id

    def validate_refresh_token(self, refresh_token: str = Depends(oauth2_scheme)) -> str:
        '''Проверить валидность refresh token'''
        user_id = self._validate_token(refresh_token, settings.jwt.refresh_token_secret_key)

        return user_id

    @staticmethod
    def _validate_token(token, token_secret_key) -> str:
        '''Проверить валидность токена и верну'''
        try:
            token_data = jwt.decode(
                token,
                token_secret_key,
                algorithms=settings.jwt.algorithm,
                audience=settings.jwt.audience,
                issuer=settings.jwt.issuer,
            )
        except jwt_exceptions.ExpiredSignatureError as e:
            user_error_message='Истёк срок действия токена'
            exception = e
        except jwt_exceptions.JWTClaimsError as e:
            user_error_message='Ошибка валидации токена'
            exception = e
        except jwt_exceptions.JWTError as e:
            user_error_message='Невалидный токен'
            exception = e
        else:
            user_id = token_data['sub']

            return user_id

        raise UnauthorizedError(
            user_error_message=user_error_message,
            system_error_message=str(exception),
            details={'token': token},
        )


jwt_validator = JWTValidator()
