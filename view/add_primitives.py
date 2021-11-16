from abc import ABC
from typing import TypeVar, Generic

import view.base as base
from logic.primitives import PrimitiveController
from view.add_item import AddItemView
from view.layout import primitive_layout as layout
from view.update_handlers import restrict_length, make_text_update_handler

T = TypeVar('T')


class AddPrimitiveView(Generic[T], AddItemView[T], ABC):
    controller: PrimitiveController[T]

    def build_layout(self):
        self.layout = layout.get_layout(self.controller.HEADER)
        super().build_layout()

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(800, 200)
        ) | kwargs)

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe(
            layout.input_name,
            restrict_length(self.controller.name_max_len),
            base.with_element(
                make_text_update_handler(lambda x: x.capitalize())
            )
        )

    def dynamic_build(self):
        super().dynamic_build()
        layout.on_finalized(self.window)

    def build_item(self, context: base.Context) -> T:
        self.item.name = context.values[layout.input_name]
        return self.item