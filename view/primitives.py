from abc import ABC
from typing import Generic
from logic.primitives import PrimitiveController
from view import base as base
from view.items import ItemsView, AddItemView, EditItemView, T
from view.layout import primitive_layout as layout
from view.update_handlers import restrict_length, make_text_update_handler
from view.utils import strip


class PrimitivesView(Generic[T], ItemsView[T], ABC):
    controller: PrimitiveController[T]

    def __init__(self):
        super().__init__()
        self.TABLE_HEADERS = [self.controller.HEADER.capitalize()]

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(500, 360)
        ) | kwargs)


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
        self.item.name = strip(context.values[layout.input_name])
        return self.item


class EditPrimitiveView(Generic[T], EditItemView[T], AddPrimitiveView[T]):
    def dynamic_build(self):
        super().dynamic_build()
        self.window[layout.input_name].update(self.item.name)