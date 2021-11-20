import inject

import view.base as base
import view.utils
from logic.roles import RolesController
from model import Role
from view import utils as utils
from view.primitives import PrimitivesView, AddPrimitiveView, EditPrimitiveView


class RolesView(PrimitivesView[Role]):
    title = view.utils.get_title("Должности")
    controller = inject.attr(RolesController)

    LABEL_CURRENT_COUNT = "Текущее количество должностей: {}"

    @base.transition
    def open_add_item_view(self):
        return AddRoleView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditRoleView(_id)


class AddRoleView(AddPrimitiveView[Role]):
    title = utils.get_title("Создание новой должности")
    controller = inject.attr(RolesController)

    def __init__(self):
        super().__init__()
        self.item = Role()


class EditRoleView(EditPrimitiveView[Role], AddRoleView):
    title = utils.get_title("Изменение названия должности")
    controller = inject.attr(RolesController)