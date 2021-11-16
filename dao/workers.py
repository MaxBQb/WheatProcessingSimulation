from dao.base import DAO
from mappers import table_to_model
from model import Worker


class WorkersDAO(DAO):
    def get_all_workers(self):
        with self._db.execute(
            "SELECT WorkerId, WorkerName, RoleName FROM worker "
            "INNER JOIN role ON worker.RoleId = role.RoleId "
            "ORDER BY worker.RoleId, WorkerName"
        ) as cursor:
            return list(cursor)

    def get_worker(self, _id: int):
        with self._db.execute(
            "SELECT * FROM worker "
            "INNER JOIN role ON worker.RoleId = role.RoleId "
            "WHERE WorkerId = %s", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), Worker)

    def get_chief_candidates(self, worker: Worker):
        with self._db.execute(
            "SELECT WorkerId, WorkerName, RoleName FROM worker "
            "INNER JOIN role ON worker.RoleId = role.RoleId "
            "WHERE WorkerId != %s "
            "ORDER BY abs(role.RoleId - %s), WorkerName",
            worker.id, worker.role_id
        ) as cursor:
            return list(cursor)

    def get_workers_count(self):
        with self._db.execute(
            "SELECT COUNT(*) FROM worker"
        ) as cursor:
            return self.single(cursor, 0)

    def add_worker(self, worker: Worker):
        with self._db.execute(
            "insert into worker (ChiefId, RoleId, WorkerName) "
            "values (%s, %s, %s)",
            worker.chief_id, worker.role_id, worker.name,
            commit=True,
        ) as cursor:
            return cursor.lastrowid

    def update_worker(self, worker: Worker):
        with self._db.execute(
            "update worker set ChiefId=%s, RoleId=%s, WorkerName=%s "
            "where WorkerId=%s",
            worker.chief_id, worker.role_id, worker.name, worker.id,
            commit=True,
        ):
            return True
