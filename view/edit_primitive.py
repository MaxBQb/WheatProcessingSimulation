from typing import TypeVar, Generic

import inject

import view.utils as utils
from logic.primitives import PrimitiveController
from logic.roles import RolesController
from model import Role
from view.add_primitives import AddPrimitiveView
from view.add_role import AddRoleView
from view.edit_item import EditItemView
from view.layout import primitive_layout as layout

T = TypeVar('T')


class EditPrimitiveView(Generic[T], EditItemView[T], AddPrimitiveView[T]):
    def dynamic_build(self):
        super().dynamic_build()
        self.window[layout.input_name].update(self.item.name)
