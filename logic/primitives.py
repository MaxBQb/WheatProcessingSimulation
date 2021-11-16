from abc import ABC
from typing import TypeVar, Generic

from logic.items import ItemsController
from model import Role

T = TypeVar('T')


class PrimitiveController(Generic[T], ItemsController[T], ABC):
    name_max_len = 40
    name_min_len = 2

    HEADER = "название"

    def validate(self, item: Role):
        if not item.name or len(item.name) < self.name_min_len:
            return f"Длина значения в поле '{self.HEADER}' не должна быть меньше {self.name_min_len}"
