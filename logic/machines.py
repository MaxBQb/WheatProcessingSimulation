import inject

from dao.machines import MachinesDAO
from logic.items import ItemsController
from logic.machine_types import MachineTypesController
from logic.table import Table
from model import Machine


class MachinesController(ItemsController[Machine]):
    source = inject.attr(MachinesDAO)
    types_controller = inject.attr(MachineTypesController)

    def get_all(self, filter_options=None):
        def to_readable_bool(data: list[tuple]):
            if not data:
                return data
            for i in range(len(data)):
                *other, last = data[i]
                data[i] = (*other, "Да" if last else "Нет")
            return data
        return super().get_all(filter_options).map(to_readable_bool)

    def get_types(self):
        return self.types_controller.get_all().map(Table)

    def validate(self, item: Machine):
        if not item.type_id:
            return "Не указан вид механизма"
