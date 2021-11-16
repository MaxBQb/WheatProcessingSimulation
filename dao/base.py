import inject
from mysql.connector import Error

from database import Database


class DAO:
    _db = inject.attr(Database)

    @staticmethod
    def single(cursor, default=None):
        return next(cursor, (default,))[0]

    @staticmethod
    def check_success(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs) or True
            except Error as e:
                return False
        return wrapper
