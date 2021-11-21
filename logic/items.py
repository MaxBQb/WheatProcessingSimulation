from dao.items import ItemsDAO
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

T = TypeVar('T')


class ItemsController(ABC, Generic[T]):
    source: ItemsDAO[T]

    def get_all(self, filter_options=None):
        return self.source.get_all(filter_options)

    def get_count(self):
        return self.source.get_count()

    @abstractmethod
    def validate(self, item: T) -> Optional[str]:
        pass

    def get_item(self, _id: int):
        return self.source.get_item(_id)

    def add_item(self, item: T):
        error = self.validate(item)
        if error:
            return error
        if not self.source.add_item(item):
            return "Вставка данных не удалась"

    def update_item(self, item: T):
        error = self.validate(item)
        if error:
            return error
        if not self.source.update_item(item):
            return "Не удалось обновить данные"

    def get_delete_confirmation_text(self, count: int):
        return "Вы точно хотите произвести удаление?\n" +\
              f"Всего удалений: {count}"

    def delete_items(self, *ids: int):
        if not self.source.delete_items(*ids):
            return "Удаление не удалось"
