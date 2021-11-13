import inject

from repository.workers import WorkersRepository


class WorkersController:
    source = inject.attr(WorkersRepository)

    def get_table(self):
        return self.source.get_all_workers()