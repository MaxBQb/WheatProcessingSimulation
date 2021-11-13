import inject

from database import Database


class DAO:
    db = inject.attr(Database)
