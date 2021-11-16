from model import Worker
from . import *
from dao.workers import WorkersDAO


class WorkersRepository:
    _dao = inject.attr(WorkersDAO)

    @live_query(tables.worker, tables.role)
    def get_all_workers(self):
        return self._dao.get_all_workers()

    @live_query(tables.worker, tables.role)
    def get_chief_candidates(self, worker: Worker):
        return self._dao.get_chief_candidates(worker)

    @live_query(tables.worker)
    def get_workers_count(self):
        return self._dao.get_workers_count()

    @live_query(tables.worker, tables.role)
    def get_worker(self, _id):
        return self._dao.get_worker(_id)

    def add_worker(self, worker: Worker):
        return self._dao.add_worker(worker)

    def update_worker(self, worker: Worker):
        return self._dao.update_worker(worker)

    def delete_workers(self, *ids: int):
        return self._dao.delete_workers(*ids)
