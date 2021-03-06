from dataclasses import dataclass

from dao.base import DAO
from dao.items import ItemsDAO, ItemFilterOptions
from dao.live_query import live_query
from mappers import table_to_model
from model import Worker


@dataclass
class WorkerFilterOptions(ItemFilterOptions):
    is_chief: bool = None
    is_available: bool = False

    _NAME_FILTERS = [
        "WorkerName",
        "RoleName",
    ]

    def __post_init__(self):
        super().__post_init__()
        self._add_toggle("""
            worker.WorkerId NOT IN (
                SELECT worker.WorkerId FROM worker
                INNER JOIN worker_to_production_line wpl ON worker.WorkerId = wpl.WorkerId
                INNER JOIN production_line pl ON wpl.ProductionLineId = pl.ProductionLineId
                WHERE pl.ProductionFinishTime IS NULL 
            )
        """, self.is_available)
        self._add_option("(worker.SubordinatesCount > 0) = %s", self.is_chief)


class WorkersDAO(ItemsDAO[Worker]):
    @live_query
    def get_all(self, filter_options: WorkerFilterOptions = None):
        where_clause, params = DAO.get_clause("WHERE", filter_options)
        with self._db.execute(
            f"SELECT * FROM view_worker worker" + where_clause,
            *params
        ) as cursor:
            return list(cursor)

    @live_query
    def get_item(self, _id: int) -> Worker:
        with self._db.execute(
            "SELECT * FROM worker "
            "INNER JOIN role ON worker.RoleId = role.RoleId "
            "WHERE WorkerId = %s", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), Worker)

    @live_query
    def get_by_production_line(self, _id: int):
        with self._db.execute("""
            SELECT w.WorkerId, WorkerName, RoleName FROM production_line 
            INNER JOIN worker_to_production_line wtpl on production_line.ProductionLineId = wtpl.ProductionLineId
            INNER JOIN worker w on wtpl.WorkerId = w.WorkerId
            INNER JOIN role r on w.RoleId = r.RoleId
            WHERE production_line.ProductionLineId = %s
        """, _id) as cursor:
            return list(cursor)

    @live_query
    def get_chief_candidates(self, worker: Worker):
        with self._db.execute(
            "SELECT WorkerId, WorkerName, RoleName FROM worker "
            "INNER JOIN role ON worker.RoleId = role.RoleId "
            "WHERE WorkerId != %s "
            "ORDER BY abs(role.RoleId - %s), WorkerName",
            worker.id, worker.role_id
        ) as cursor:
            return list(cursor)

    @live_query
    def get_count(self) -> int:
        with self._db.execute(
            "SELECT COUNT(*) FROM worker"
        ) as cursor:
            return self.single(cursor, 0)

    @DAO.check_success
    def add_item(self, item: Worker) -> int:
        with self._db.execute(
            "insert into worker (ChiefId, RoleId, WorkerName) "
            "values (%s, %s, %s)",
            item.chief_id, item.role_id, item.name,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    @DAO.check_success
    def update_item(self, item: Worker):
        with self._db.execute(
            "update worker set ChiefId=%s, RoleId=%s, WorkerName=%s "
            "where WorkerId=%s",
            item.chief_id, item.role_id, item.name, item.id,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    def _delete_item(self, cursor, _id: int):
        cursor.execute(
            "delete from worker where WorkerId = %s",
            (_id,)
        )
