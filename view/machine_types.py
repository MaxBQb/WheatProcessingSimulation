import inject

import view.base as base
import view.utils
from logic.machine_types import MachineTypesController
from model import MachineType
from view.add_machine_type import AddMachineTypeView
from view.edit_machine_type import EditMachineTypeView
from view.primitives import PrimitivesView


class MachineTypesView(PrimitivesView[MachineType]):
    title = view.utils.get_title("Виды станков")
    controller = inject.attr(MachineTypesController)

    LABEL_CURRENT_COUNT = "Текущее число видов: {}"

    @base.transition
    def open_add_item_view(self):
        return AddMachineTypeView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditMachineTypeView(_id)
