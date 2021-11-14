from dao.base import DAO


class WorkersDAO(DAO):
    def get_all_workers(self):
        with self._db.execute(
            "SELECT WorkerId, WorkerName, RoleName FROM worker "
            "INNER JOIN role ON worker.RoleId = role.RoleId"
        ) as cursor:
            return list(cursor)

    def get_workers_count(self):
        with self._db.execute(
            "SELECT COUNT(*) FROM worker"
        ) as cursor:
            return self.single(cursor, 0)
