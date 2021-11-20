import inject

import view.base as base
import view.utils
from logic.machine_types import MachineTypesController
from model import MachineType
from view import utils as utils
from view.primitives import PrimitivesView, AddPrimitiveView, EditPrimitiveView


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


class AddMachineTypeView(AddPrimitiveView[MachineType]):
    title = utils.get_title("Добавление нового вида станков")
    controller = inject.attr(MachineTypesController)

    def __init__(self):
        super().__init__()
        self.item = MachineType()


class EditMachineTypeView(EditPrimitiveView[MachineType], AddMachineTypeView):
    title = utils.get_title("Изменение названия вида станка")
    controller = inject.attr(MachineTypesController)