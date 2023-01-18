from collections.abc import Sequence
from typing import Any, TypeVar

from sqlalchemy import delete, insert, select, update, func
from sqlalchemy.sql.dml import (
    Delete as DeleteQuery,
    Insert as InsertQuery,
    Update as UpdateQuery,
)
from sqlalchemy.engine.row import Row as SQLAlchemyRow
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select as SelectQuery

from core.errors.app_errors import ResourceConflictError, ResourceNotFoundError
from core.orm import Base
from core.repositories.enums import SQLOperators
from core.repositories.utils import convert_sqlalchemy_row_to_model


Model = TypeVar('Model', bound=Base)
WhereCondition = tuple[str, SQLOperators, Any]


class Repository:
    '''Репозиторный слой для работы с БД'''

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add_obj_to_session(self, model: type[Model], data: dict[str, Any]) -> Model:
        '''Добавить объект в сессию для его создания при следующем коммите'''
        obj = model(**data)
        self.session.add(obj)

        return obj

    async def commit(self) -> None:
        '''Закоммитить изменения из сессии'''
        try:
            await self.session.commit()
        except IntegrityError as exception:
            raise ResourceConflictError(
                user_error_message='Создаваемый объект нарушает существующие ограничения данных',
                system_error_message=str(exception),
            )

    async def delete(
        self,
        *,
        model: type[Model],
        conditions: Sequence[WhereCondition],
    ) -> None:
        '''Удалить объекты из БД по условию'''
        query = self._generate_delete_query(model, conditions)

        await self.session.execute(query)

    async def insert(
        self,
        *,
        model: type[Model],
        data: dict[str, Any] | list[dict],
    ) -> None:
        '''Создать(вставить) запись в БД'''
        query = self._generate_insert_query(model, data)

        try:
            await self.session.execute(query)
        except IntegrityError as exception:
            raise ResourceConflictError(
                user_error_message='Создаваемый объект нарушает существующие ограничения данных',
                system_error_message=str(exception),
            )

    async def rollback(self) -> None:
        '''Откатить изменения сессии'''
        await self.session.rollback()

    async def select_list(
        self,
        *,
        model: type[Model],
        conditions: Sequence[WhereCondition],
        joins: Sequence[Model] | None = None,
        joins_conditions: dict[Model, Sequence[WhereCondition]] | None = None,
    ) -> list[Model]:
        '''Выполнить SELECT данных из нужной таблицы для получения
        списка объектов

        '''
        results = await self._select(model, conditions, joins, joins_conditions)

        return results.scalars().all()

    async def select_one(
        self,
        *,
        model: type[Model],
        conditions: Sequence[WhereCondition],
        joins: Sequence[Model] | None = None,
        joins_conditions: dict[Model, Sequence[WhereCondition]] | None = None,
    ) -> Model:
        '''Выполнить SELECT данных из нужной таблицы для получения
        одного объекта

        '''
        results = await self._select(model, conditions, joins, joins_conditions)

        try:
            return results.scalar_one()
        except NoResultFound as exception:
            raise ResourceNotFoundError(
                user_error_message='Запрашиваемый объект не найден',
                system_error_message=str(exception),
                details={
                    'conditions': {
                        str(condition[0]): str(condition[2]) for condition in conditions
                    },
                },
            )

    async def select_count(
        self,
        *,
        model: type[Model],
        conditions: Sequence[WhereCondition] | None = None,
    ) -> int:
        '''Получить количество записей'''
        conditions = self._parse_conditions(model, conditions)
        query = select(func.count()).select_from(model).where(conditions)
        return await self.select_scalar_one(query=query)

    async def update(
        self,
        *,
        model: type[Model],
        data: dict[str, Any],
        conditions: Sequence[WhereCondition],
    ) -> None:
        '''Обновить объекты в БД, соответсвующие условиям'''
        query = self._generate_update_query(model, data, conditions)

        try:
            await self.session.execute(query)
        except IntegrityError as exception:
            raise ResourceConflictError(
                user_error_message='Обновление объекта нарушает существующие ограничения данных',
                system_error_message=str(exception),
            )

    @convert_sqlalchemy_row_to_model
    async def update_and_return_one(
        self,
        *,
        model: type[Model],
        data: dict[str, Any],
        conditions: Sequence[WhereCondition],
    ) -> SQLAlchemyRow:
        '''Обновить и вернуть один объект из БД'''
        query = self._generate_update_query(model, data, conditions)

        results = await self.session.execute(query.returning(model))

        try:
            return results.one()
        except NoResultFound as exception:
            raise ResourceNotFoundError(
                user_error_message='Объект не может быть обновлен, так как не найден',
                system_error_message=str(exception),
                details={
                    'conditions': {
                        str(condition[0]): str(condition[2]) for condition in conditions
                    },
                },
            )

    async def select_scalar_one(self, *, query: SelectQuery) -> Model:
        '''Выполнить SELECT данных из нужной таблицы для получения
        одного объекта

        '''
        results = await self.session.execute(query)
        try:
            return results.unique().scalar_one()
        except NoResultFound as exception:
            raise ResourceNotFoundError(
                user_error_message='Запрашиваемый объект не найден',
                system_error_message=str(exception),
                details={},
            )

    def _generate_delete_query(
        self,
        model: type[Model],
        conditions: Sequence[WhereCondition],
    ) -> DeleteQuery:
        '''Составить DELETE запрос в соответсвии с условиями'''
        parsed_conditions = self._parse_conditions(model, conditions)
        query = delete(model).where(*parsed_conditions)

        return query

    def _generate_insert_query(
        self,
        model: type[Model],
        data: dict[str, Any],
    ) -> InsertQuery:
        '''Составить INSERT запрос с нужными данными'''
        query = insert(model).values(data)

        return query

    def _generate_select_query(
        self,
        model: type[Model],
        conditions: Sequence[WhereCondition],
        joins: Sequence[Model] | None = None,
        joins_conditions: dict[Model, Sequence[WhereCondition]] | None = None,
    ) -> SelectQuery:
        '''Составить SELECT запрос в соответсвии с условиями'''
        parsed_conditions = self._parse_conditions(model, conditions)
        query: SelectQuery = select(model).where(*parsed_conditions)
        query = self._join_and_filter(query, joins=joins, joins_conditions=joins_conditions)

        return query

    def _generate_update_query(
        self,
        model: type[Model],
        data: dict[str, Any],
        conditions: Sequence[WhereCondition],
    ) -> UpdateQuery:
        '''Сгенерировать объект запроса на обновление'''
        parsed_conditions = self._parse_conditions(model, conditions)
        query = update(model).values(**data).where(*parsed_conditions)

        return query

    @staticmethod
    def _parse_conditions(
        model: type[Model],
        conditions: Sequence[WhereCondition],
    ) -> list[tuple]:
        '''Распарсить переданные условия запроса и подготовить их
        для работы с ORM

        '''
        parsed_conditions = []

        for column, sql_operator, value in conditions:
            if sql_operator == SQLOperators.EQ:
                parsed_conditions.append(getattr(model, column) == value)
            elif sql_operator == SQLOperators.IN:
                parsed_conditions.append(getattr(model, column).in_(value))
            elif sql_operator == SQLOperators.NE:
                parsed_conditions.append(getattr(model, column) != value)
            else:
                raise NotImplementedError('Operator is not supported')
        print('*' * 100, parsed_conditions)
        return parsed_conditions

    def _join_and_filter(
        self,
        query: SelectQuery,
        joins: Sequence[Model] | None = None,
        joins_conditions: dict[Model, Sequence[WhereCondition]] | None = None,
    ) -> SelectQuery:
        ''' Выполнить join с таблицами указанными в joins
        и применить к джойнам фильтрацию из joins_conditions

        '''
        joins = joins or []
        for join in joins:
            # FIXME: здесь не всегда должен быть isouter=True
            query = query.join(join, isouter=True)

        joins_conditions = joins_conditions or {}
        for join_model in joins_conditions:
            parsed_join_conditions = self._parse_conditions(
                join_model,
                joins_conditions[join_model],
            )
            query = query.where(*parsed_join_conditions)

        return query

    async def _select(
        self,
        model: type[Model],
        conditions: Sequence[WhereCondition],
        joins: Sequence[Model] | None = None,
        joins_conditions: dict[Model, Sequence[WhereCondition]] | None = None,
    ) -> ChunkedIteratorResult:
        '''Выполнить SELECT запрос с нужными условиями'''
        query = self._generate_select_query(model, conditions, joins, joins_conditions)

        results = await self.session.execute(query)

        return results
