from dao.base import DAO


class ChangesDAO(DAO):
    def get_all_changes(self, update_interval: int):
        with self._db.execute(
            "SELECT * FROM changes "
            "WHERE LastChange > date_sub(now(), INTERVAL %s second)",
            update_interval
        ) as cursor:
            return list(cursor)
