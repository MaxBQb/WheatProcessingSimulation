from dao.base import DAO
from typing import TypeVar, Generic
from abc import ABC, abstractmethod


T = TypeVar('T')


class ItemsDAO(DAO, Generic[T], ABC):

    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def get_item(self, _id: int) -> T:
        pass

    @abstractmethod
    def get_count(self) -> int:
        pass

    @DAO.check_success
    @abstractmethod
    def add_item(self, item: T) -> int:
        pass

    @DAO.check_success
    @abstractmethod
    def update_item(self, item: T):
        pass

    @DAO.check_success
    def delete_items(self, *ids: int):
        with self._db.cursor(True) as cursor:
            for _id in ids:
                self._delete_item(cursor, _id)

    @abstractmethod
    def _delete_item(self, cursor, _id: int):
        pass
