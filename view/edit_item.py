from abc import ABC
from copy import deepcopy
from typing import TypeVar, Generic

import view.base as base
from view.add_item import AddItemView

T = TypeVar('T')


class EditItemView(Generic[T], AddItemView[T], ABC):
    def __init__(self, _id: int):
        super().__init__()
        self.item: T = self.controller.get_item(_id).value
        self.item_original: T = deepcopy(self.item)

    def on_submit(self, context: base.Context):
        item = self.build_item(context)
        if self.item_original == item:
            return
        result = self.controller.update_item(item)
        if self.show_error(result):
            return
        self.close()
