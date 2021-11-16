import inject

import view.utils as utils
from logic.roles import RolesController
from model import Role
from view.add_primitives import AddPrimitiveView


class AddRoleView(AddPrimitiveView[Role]):
    title = utils.get_title("Создание новой должности")
    controller = inject.attr(RolesController)

    def __init__(self):
        super().__init__()
        self.item = Role()
