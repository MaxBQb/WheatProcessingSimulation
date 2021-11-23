from dataclasses import dataclass

from dao.base import DAO, OptionalQuery
from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from dao.live_query import live_query


T = TypeVar('T')


@dataclass
class ItemFilterOptions(OptionalQuery):
    name: str = None

    _NAME_FILTERS = []

    def __post_init__(self):
        super().__init__("AND")
        self.name = self.name or None
        if self._NAME_FILTERS:
            name_filter = self._NamesOptions(self._NAME_FILTERS, self.name)
            self._add_toggle_group(name_filter, self.name)

    @dataclass
    class _NamesOptions(OptionalQuery):
        columns: list[str]
        name: str

        def __post_init__(self):
            super().__init__("OR")
            for column in self.columns:
                self._add_option(f"""
                    {column} like CONCAT('%', %s, '%')
                """, self.name)


class ItemsDAO(ABC, Generic[T], DAO):

    @live_query
    @abstractmethod
    def get_all(self, filter_options: 'OptionalQuery' = None) -> list:
        pass

    @live_query
    @abstractmethod
    def get_item(self, _id: int) -> T:
        pass

    @live_query
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

