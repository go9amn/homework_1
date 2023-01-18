from datetime import datetime, timedelta, timezone

from jose import jwt

from core.settings.settings import settings


class JWTIssuer:
    '''Класс для создания JWT токенов'''
    # TODO: скорее всего, позже надо будет зашить данные о юзере в токен
    def issue_tokens(self, user_id: str) -> dict:
        '''Выпустить пару JWT токенов(access и refresh)'''
        access_token_data = self._arrange_token_data(
            {settings.jwt.access_token_exp_in_time_period: settings.jwt.access_token_exp_in_value},
            user_id,
        )
        refresh_token_data = self._arrange_token_data(
            {settings.jwt.refresh_token_exp_in_time_period: settings.jwt.refresh_token_exp_in_value},
            user_id,
        )

        return {
            'access_token': self._sign_token(
                access_token_data,
                settings.jwt.access_token_secret_key,
            ),
            'exp': access_token_data['exp'],
            'refresh_token': self._sign_token(
                refresh_token_data,
                settings.jwt.refresh_token_secret_key,
            ),
        }

    def _arrange_token_data(self, token_exp_data: dict[str, int], user_id: str) -> dict:
        '''Сгруппировать данные токена'''
        token_data = {
            'aud': settings.jwt.audience,
            'exp': self._calculate_exp_timestamp(token_exp_data),
            'iat': datetime.now(timezone.utc),
            'iss': settings.jwt.issuer,
            'sub': user_id,
        }

        return token_data

    @staticmethod
    def _calculate_exp_timestamp(token_exp_data: dict[str, int]) -> int:
        '''Расчитать timestamp в UTC, когда токен перестанет
        быть валидным
        '''
        token_exp_timedelta = timedelta(
            **token_exp_data,
        )
        utc_datetime_now = datetime.now(timezone.utc)
        token_exp_timestamp = int((utc_datetime_now + token_exp_timedelta).timestamp())

        return token_exp_timestamp

    @staticmethod
    def _sign_token(token_data: dict, secret_key: str) -> str:
        '''Закодировать данные токена, используя нужный алгоритм
        и подпись

        '''
        token = jwt.encode(
            token_data,
            secret_key,
            settings.jwt.algorithm,
        )

        return token


jwt_issuer = JWTIssuer()
