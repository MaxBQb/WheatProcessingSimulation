from dao.base import DAO


class RolesDAO(DAO):
    def get_roles(self):
        with self._db.execute(
            "SELECT * FROM role"
        ) as cursor:
            return list(cursor)
