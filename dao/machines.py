from dataclasses import dataclass

from dao.base import DAO
from dao.items import ItemsDAO, ItemFilterOptions
from dao.live_query import live_query
from mappers import table_to_model
from model import Machine


@dataclass
class MachineFilterOptions(ItemFilterOptions):
    is_powered: bool = None
    is_available: bool = False

    _NAME_FILTERS = ["MachineTypeName"]

    def __post_init__(self):
        super().__post_init__()
        self._add_toggle("""
            machine.MachineId NOT IN (
                SELECT machine.MachineId FROM machine
                INNER JOIN machine_to_production_line mpl ON machine.MachineId = mpl.MachineId
                INNER JOIN production_line pl ON mpl.ProductionLineId = pl.ProductionLineId
                WHERE pl.ProductionFinishTime IS NULL 
            )
            """, self.is_available)
        self._add_option("machine.IsPowered = %s", self.is_powered)


class MachinesDAO(ItemsDAO[Machine]):
    @live_query
    def get_all(self, filter_options: MachineFilterOptions = None):
        where_clause, params = DAO.get_clause("WHERE", filter_options)
        with self._db.execute(
            f"SELECT * FROM view_machine machine" + where_clause,
            *params
        ) as cursor:
            return list(cursor)

    @live_query
    def get_item(self, _id: int) -> Machine:
        with self._db.execute(
            "SELECT * FROM machine "
            "INNER JOIN machine_type ON machine.MachineTypeId = machine_type.MachineTypeId "
            "WHERE MachineId = %s", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), Machine)

    @live_query
    def get_by_production_line(self, _id: int):
        with self._db.execute("""
            SELECT m.MachineId, MachineTypeName FROM production_line 
            INNER JOIN machine_to_production_line mtpl on production_line.ProductionLineId = mtpl.ProductionLineId
            INNER JOIN machine m on mtpl.MachineId = m.MachineId
            INNER JOIN machine_type mt on m.MachineTypeId = mt.MachineTypeId
            WHERE production_line.ProductionLineId = %s
        """, _id) as cursor:
            return list(cursor)

    @live_query
    def get_count(self) -> int:
        with self._db.execute(
            "SELECT COUNT(*) FROM machine"
        ) as cursor:
            return self.single(cursor, 0)

    @DAO.check_success
    def add_item(self, item: Machine) -> int:
        with self._db.execute(
            "insert into machine (MachineTypeId, IsPowered) "
            "values (%s, %s)",
            item.type_id, item.is_powered,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    @DAO.check_success
    def update_item(self, item: Machine):
        with self._db.execute(
            "update machine set MachineTypeId=%s, IsPowered=%s "
            "where MachineId=%s",
            item.type_id, item.is_powered, item.id,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    def _delete_item(self, cursor, _id: int):
        cursor.execute(
            "delete from machine where MachineId = %s",
            (_id,)
        )
