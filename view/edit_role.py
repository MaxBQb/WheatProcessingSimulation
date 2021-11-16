import inject

import view.utils as utils
from logic.roles import RolesController
from model import Role
from view.add_role import AddRoleView
from view.edit_primitive import EditPrimitiveView


class EditRoleView(EditPrimitiveView[Role], AddRoleView):
    title = utils.get_title("Изменение названия должности")
    controller = inject.attr(RolesController)
