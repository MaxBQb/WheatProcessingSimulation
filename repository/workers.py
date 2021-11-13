import inject

from dao.workers import WorkersDAO


class WorkersRepository:
    dao = inject.attr(WorkersDAO)

    def get_all_workers(self):
        return self.dao.get_all_workers()
