from datetime import datetime

import inject

from dao.machines import MachineFilterOptions
from dao.production_lines import ProductionLinesDAO, ProductionLineFilterOptions
from dao.resources import ResourceFilterOptions
from dao.workers import WorkerFilterOptions
from logic.items import ItemsController
from logic.machines import MachinesController
from logic.resources import ResourcesController
from logic.roles import RolesController
from logic.standards import StandardsController
from logic.table import Table
from logic.workers import WorkersController
from model import ProductionLine


class ProductionLinesController(ItemsController[ProductionLine]):
    source = inject.attr(ProductionLinesDAO)
    standards_controller = inject.attr(StandardsController)
    workers_controller = inject.attr(WorkersController)
    machines_controller = inject.attr(MachinesController)
    resources_controller = inject.attr(ResourcesController)
    filter_type = ProductionLineFilterOptions
    date_format = '%d.%m.%Y %H:%M:%S'

    def get_standards(self):
        return self.standards_controller.get_all().map(Table)

    def get_available_workers(self):
        return self.workers_controller.get_all(WorkerFilterOptions(
            is_available=True
        )).map(lambda data: Table(
            [(_id, f"{name}, {role}")
             for _id, name, role, *_ in data]
        ))

    def get_used_workers(self, production_line: ProductionLine):
        return self.workers_controller.get_by_production_line(
            production_line
        ).map(lambda data: Table(
            [(_id, f"{name}, {role}")
             for _id, name, role, *_ in data]
        ))

    def get_available_resources(self):
        return self.resources_controller.get_all(ResourceFilterOptions(
            is_available=True
        )).map(lambda data: Table(
            [(_id, f"{name}, {description[:22]}" if description else name)
             for _id, name, description in data]
        ))

    def get_used_resources(self, production_line: ProductionLine):
        return self.resources_controller.get_resources_by_production_line(
            production_line
        ).map(lambda data: Table(
            [(_id, f"{name}, {description[:22]}" if description else name)
             for _id, name, description in data]
        ))

    def get_produced_results(self, production_line: ProductionLine):
        return self.resources_controller.get_results_by_production_line(
            production_line
        ).map(lambda data: Table(
            [(_id, f"{name}, {description[:22]}" if description else name)
             for _id, name, description in data]
        ))

    def get_results(self):
        return self.resources_controller.get_all(ResourceFilterOptions(
            is_planned=True,
            is_producible=True,
        )).map(lambda data: Table(
            [(_id, f"{name}, {description[:22]}" if description else name)
             for _id, name, description in data]
        ))

    def get_available_machines(self):
        return self.machines_controller.get_all(MachineFilterOptions(
            is_available=True,
            is_powered=True,
        )).map(Table)

    def get_used_machines(self, production_line: ProductionLine):
        return self.machines_controller.get_by_production_line(
            production_line
        ).map(Table)

    def validate_update(self, item: ProductionLine):
        if not item.standard_id:
            return "Должен быть указан стандарт производства"

        start = item.production_start_time or datetime.now()
        if item.production_finish_time and (
                (item.production_finish_time - start).total_seconds() < 10
        ):
            return "Процесс не может длиться менее 10 секунд"

    def validate(self, item: ProductionLine):
        if not item.results:
            return "Не указаны результаты производства"

        if not item.resources:
            return "Не указаны использованные ресурсы"

        if not item.workers:
            return "Не указаны исполнители"

        if not item.machines:
            return "Не указаны используемые станки"

        return self.validate_update(item)
