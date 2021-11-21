from typing import Callable, Any, Union

import inject
from mysql.connector import Error

from database import Database


class DAO:
    _db = inject.attr(Database)

    @staticmethod
    def single(cursor, default=None):
        return next(cursor, (default,))[0]

    @staticmethod
    def check_success(func) -> Callable[..., Union[bool, Any]]:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs) or True
            except Error:
                return False
        return wrapper

    @staticmethod
    def get_clause(clause: str, optional_query: 'OptionalQuery' = None):
        if optional_query is None or not optional_query.query:
            return "", []
        return f" {clause} {optional_query.query}", optional_query.params


class OptionalQuery:
    def __init__(self, default_operator: str):
        self._default_operator = default_operator
        self.query = ""
        self.params = []

    def _add_option(self, statement: str, value, operator: str = None):
        if value is None:
            return
        self.__add(statement, value, operator)
        self.params.append(value)

    def _add_toggle(self, statement: str, value: bool, operator: str = None):
        self.__add(statement, value or None, operator)

    def __add(self, statement: str, value, operator: str = None):
        if value is None:
            return
        if self.query:
            self.query += f' {(operator or self._default_operator)} '
        self.query += statement.strip()  # .format(value)
