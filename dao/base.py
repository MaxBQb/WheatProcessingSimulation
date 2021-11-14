import inject

from database import Database


class DAO:
    _db = inject.attr(Database)

    @staticmethod
    def single(cursor, default=None):
        return next(cursor, (default,))[0]