from . import *
from dao.workers import WorkersDAO


class WorkersRepository:
    _dao = inject.attr(WorkersDAO)

    @live_query(tables.worker, tables.role)
    def get_all_workers(self):
        return self._dao.get_all_workers()
