import inject

import view.utils as utils
from logic.machine_types import MachineTypesController
from model import MachineType
from view.add_primitives import AddPrimitiveView


class AddMachineTypeView(AddPrimitiveView[MachineType]):
    title = utils.get_title("Добавление нового вида станков")
    controller = inject.attr(MachineTypesController)

    def __init__(self):
        super().__init__()
        self.item = MachineType()
