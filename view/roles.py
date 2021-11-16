import inject

import view.base as base
import view.utils
from logic.roles import RolesController
from model import Role
from view.add_role import AddRoleView
from view.edit_role import EditRoleView
from view.primitives import PrimitivesView


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

