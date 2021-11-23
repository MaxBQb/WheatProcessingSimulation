from datetime import datetime
from typing import Optional

from dao.base import DAO


class ChangesDAO(DAO):
    def get_last_change(self) -> Optional[datetime]:
        with self._db.execute(
            "SELECT MAX(LastChange) FROM changes"
        ) as cursor:
            return DAO.single(cursor, None)
