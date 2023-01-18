from typing import Any

from pydantic import BaseModel


class BaseSchema(BaseModel):
    '''Кастомная pydantic модель для отображения
    данных в схеме в нужном формате

    '''
    class Config:

        @staticmethod
        def schema_extra(
            schema: dict[str, Any], model: type['BaseSchema'],
            ) -> None:
            '''Добавить примеры для дат в схему'''
            properties = schema.get('properties', {})

            # Отображать даты в нужном формате
            for field_name in properties:
                if properties[field_name].get('format') == 'date-time':
                    properties[field_name]['example'] = '2022-06-06T06-06-06'
                    properties[field_name]['example'] = '2022-06-06T06-06-06'

            # Отображать поля с ценами в нужном формате
            for field_name in properties:
                if field_name in ('price', ):
                    properties[field_name] = {
                        'example': 666.66,
                        'format': 'Decimal(10, 2)',
                        'type': 'number'
                    }
