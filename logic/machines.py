import inject

from dao.machines import MachinesDAO, MachineFilterOptions
from logic.items import ItemsController
from logic.machine_types import MachineTypesController
from logic.table import Table
from model import Machine, ProductionLine


class MachinesController(ItemsController[Machine]):
    source = inject.attr(MachinesDAO)
    filter_type = MachineFilterOptions
    types_controller = inject.attr(MachineTypesController)

    def get_types(self):
        return self.types_controller.get_all().map(Table)

    def get_by_production_line(self, production_line: ProductionLine):
        return self.source.get_by_production_line(
            production_line.id
        )

    def validate(self, item: Machine):
        if not item.type_id:
            return "Не указан вид механизма"
