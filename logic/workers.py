import inject

from dao.workers import WorkersDAO, WorkerFilterOptions
from logic.items import ItemsController
from logic.roles import RolesController
from logic.table import Table
from model import Worker, ProductionLine


class WorkersController(ItemsController[Worker]):
    source = inject.attr(WorkersDAO)
    roles_controller = inject.attr(RolesController)
    filter_type = WorkerFilterOptions

    name_max_len = 60
    name_min_len = 2

    def get_chief_candidates(self, worker: Worker):
        return (
            self.source
            .get_chief_candidates(worker)
            .map(lambda data: Table(
                [(None, "Нет")] +
                [(_id, f"{name}, {role}")
                 for _id, name, role in data]))
        )

    def get_roles(self):
        return self.roles_controller.get_all().map(Table)

    def get_by_production_line(self, production_line: ProductionLine):
        return self.source.get_by_production_line(
            production_line.id
        )

    def validate(self, item: Worker):
        if not item.name or len(item.name) < self.name_min_len:
            return f"Длина ФИО не должна быть меньше {self.name_min_len}"

        if not item.role_id:
            return "Не указана должность"
