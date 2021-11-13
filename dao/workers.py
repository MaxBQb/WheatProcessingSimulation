from dao.base import DAO


class WorkersDAO(DAO):
    def get_all_workers(self):
        with self.db.execute(
            "SELECT WorkerId, WorkerName, RoleName FROM worker "
            "INNER JOIN role ON worker.RoleId = role.RoleId"
        ) as cursor:
            return list(cursor)
