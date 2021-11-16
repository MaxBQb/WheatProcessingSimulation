from abc import ABC, abstractmethod
from typing import TypeVar, Generic

import view.base as base
from logic.items import ItemsController
from view.layout import submit_button

T = TypeVar('T')


class AddItemView(ABC, Generic[T], base.BaseInteractiveWindow):
    controller: ItemsController[T]

    def __init__(self):
        super().__init__()
        self.item: T

    def build_layout(self):
        self.layout += [submit_button.get_layout()]

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe(
            submit_button.button_submit,
            self.on_submit
        )

    @abstractmethod
    def build_item(self, context: base.Context) -> T:
        pass

    def on_submit(self, context: base.Context):
        item = self.build_item(context)
        result = self.controller.add_item(item)
        if self.show_error(result):
            return
        self.close()
