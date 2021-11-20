from dao.base import DAO
from dao.items import ItemsDAO
from dao.live_query import live_query, tables
from mappers import table_to_model
from model import Worker


class WorkersDAO(ItemsDAO[Worker]):
    @live_query(tables.worker, tables.role)
    def get_all(self):
        with self._db.execute("""
            SELECT * FROM view_workers worker  
            ORDER BY RoleName, WorkerName
        """) as cursor:
            return list(cursor)

    @live_query(
        tables.worker,
        tables.role,
        tables.worker_to_production_line,
        tables.production_line)
    def get_available(self):
        with self._db.execute("""
            SELECT * FROM view_workers worker
            WHERE worker.WorkerId NOT IN (
                SELECT worker.WorkerId FROM worker
                INNER JOIN worker_to_production_line wpl ON worker.WorkerId = wpl.WorkerId
                INNER JOIN production_line pl ON wpl.ProductionLineId = pl.ProductionLineId
                WHERE pl.ProductionFinishTime IS NULL 
            )
        """) as cursor:
            return list(cursor)

    @live_query(tables.worker, tables.role)
    def get_chiefs(self):
        with self._db.execute("""
            SELECT * FROM view_workers worker
            WHERE worker.SubordinatesCount > 0   
        """) as cursor:
            return list(cursor)

    @live_query(
        tables.worker,
        tables.role,
        tables.worker_to_production_line,
        tables.production_line)
    def get_available_chiefs(self):
        with self._db.execute("""
            SELECT * FROM view_workers worker
            WHERE worker.WorkerId NOT IN (
                SELECT worker.WorkerId FROM worker
                INNER JOIN worker_to_production_line wpl ON worker.WorkerId = wpl.WorkerId
                INNER JOIN production_line pl ON wpl.ProductionLineId = pl.ProductionLineId
                WHERE pl.ProductionFinishTime IS NULL 
            ) 
            AND worker.SubordinatesCount > 0
        """) as cursor:
            return list(cursor)

    @live_query(tables.worker, tables.role)
    def get_item(self, _id: int) -> Worker:
        with self._db.execute(
            "SELECT * FROM worker "
            "INNER JOIN role ON worker.RoleId = role.RoleId "
            "WHERE WorkerId = %s", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), Worker)

    @live_query(tables.worker, tables.role)
    def get_chief_candidates(self, worker: Worker):
        with self._db.execute(
            "SELECT WorkerId, WorkerName, RoleName FROM worker "
            "INNER JOIN role ON worker.RoleId = role.RoleId "
            "WHERE WorkerId != %s "
            "ORDER BY abs(role.RoleId - %s), WorkerName",
            worker.id, worker.role_id
        ) as cursor:
            return list(cursor)

    @live_query(tables.worker)
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
