from dao.base import DAO
from model import Worker


class WorkersDAO(DAO):
    def get_all_workers(self):
        with self._db.execute(
            "SELECT WorkerId, WorkerName, RoleName FROM worker "
            "INNER JOIN role ON worker.RoleId = role.RoleId"
        ) as cursor:
            return list(cursor)

    def get_chief_candidates(self, worker: Worker):
        with self._db.execute(
            "SELECT WorkerId, WorkerName, RoleName FROM worker "
            "INNER JOIN role ON worker.RoleId = role.RoleId "
            "WHERE WorkerId != %s "
            "ORDER BY abs(role.RoleId - %s)",
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
