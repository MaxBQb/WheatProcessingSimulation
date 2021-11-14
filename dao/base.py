import inject

from database import Database


class DAO:
    _db = inject.attr(Database)
