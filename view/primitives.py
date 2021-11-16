from abc import ABC
from typing import Generic, TypeVar

from logic.primitives import PrimitiveController
from view.items import ItemsView

T = TypeVar('T')


class PrimitivesView(Generic[T], ItemsView[T], ABC):
    controller: PrimitiveController[T]

    def __init__(self):
        super().__init__()
        self.TABLE_HEADERS = [self.controller.HEADER.capitalize()]

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(500, 360)
        ) | kwargs)
