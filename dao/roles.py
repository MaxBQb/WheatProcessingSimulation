from dao.base import DAO
from dao.items import ItemsDAO
from dao.live_query import live_query
from mappers import table_to_model
from model import Role


class RolesDAO(ItemsDAO[Role]):
    @live_query
    def get_all(self, _=None):
        with self._db.execute(
            "SELECT * FROM role"
        ) as cursor:
            return list(cursor)

    @live_query
    def get_item(self, _id: int) -> Role:
        with self._db.execute(
            "SELECT * FROM role "
            "WHERE RoleId = %s", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), Role)

    @live_query
    def get_count(self) -> int:
        with self._db.execute(
            "SELECT COUNT(*) FROM role"
        ) as cursor:
            return self.single(cursor, 0)

    @DAO.check_success
    def add_item(self, item: Role) -> int:
        with self._db.execute(
            "insert into role (RoleName) "
            "values (%s)", item.name,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    @DAO.check_success
    def update_item(self, item: Role):
        with self._db.execute(
                "update role set RoleName=%s "
                "where RoleId=%s",
                item.name, item.id,
                commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    def _delete_item(self, cursor, _id: int):
        cursor.execute(
            "delete from role where RoleId = %s",
            (_id,)
        )
