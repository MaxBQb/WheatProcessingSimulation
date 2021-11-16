from dao.base import DAO
from dao.live_query import live_query, tables


class RolesDAO(DAO):
    @live_query(tables.role)
    def get_roles(self):
        with self._db.execute(
            "SELECT * FROM role"
        ) as cursor:
            return list(cursor)
