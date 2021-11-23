from dao.base import DAO
from dao.items import ItemsDAO
from dao.live_query import live_query
from mappers import table_to_model
from model import MachineType


class MachineTypesDAO(ItemsDAO[MachineType]):
    @live_query
    def get_all(self, _=None):
        with self._db.execute(
            "SELECT * FROM machine_type"
        ) as cursor:
            return list(cursor)

    @live_query
    def get_item(self, _id: int) -> MachineType:
        with self._db.execute(
            "SELECT * FROM machine_type "
            "WHERE MachineTypeId = %s", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), MachineType)

    @live_query
    def get_count(self) -> int:
        with self._db.execute(
            "SELECT COUNT(*) FROM machine_type"
        ) as cursor:
            return self.single(cursor, 0)

    @DAO.check_success
    def add_item(self, item: MachineType) -> int:
        with self._db.execute(
            "insert into machine_type (MachineTypeName) "
            "values (%s)", item.name,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    @DAO.check_success
    def update_item(self, item: MachineType):
        with self._db.execute(
                "update machine_type set MachineTypeName=%s "
                "where MachineTypeId=%s",
                item.name, item.id,
                commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    def _delete_item(self, cursor, _id: int):
        cursor.execute(
            "delete from machine_type where MachineTypeId = %s",
            (_id,)
        )
