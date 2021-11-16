import inject

import view.utils as utils
from logic.machine_types import MachineTypesController
from model import MachineType
from view.add_machine_type import AddMachineTypeView
from view.edit_primitive import EditPrimitiveView


class EditMachineTypeView(EditPrimitiveView[MachineType], AddMachineTypeView):
    title = utils.get_title("Изменение названия вида станка")
    controller = inject.attr(MachineTypesController)
