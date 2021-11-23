from dataclasses import dataclass

from dao.base import DAO
from dao.items import ItemsDAO, ItemFilterOptions
from dao.live_query import live_query
from mappers import table_to_model
from model import ResourceType


@dataclass
class ResourceTypeFilterOptions(ItemFilterOptions):
    _NAME_FILTERS = ["ResourceTypeName"]


class ResourceTypesDAO(ItemsDAO[ResourceType]):
    @live_query
    def get_all(self, filter_options: ResourceTypeFilterOptions = None):
        where_clause, params = DAO.get_clause("WHERE", filter_options)
        with self._db.execute(
            f"SELECT ResourceTypeId, ResourceTypeName, IsProducible FROM resource_type " + where_clause,
            *params
        ) as cursor:
            return list(cursor)

    @live_query
    def get_item(self, _id: int) -> ResourceType:
        with self._db.execute(
            "SELECT * FROM resource_type "
            "WHERE ResourceTypeId = %s", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), ResourceType)

    @live_query
    def get_count(self) -> int:
        with self._db.execute(
            "SELECT COUNT(*) FROM resource_type"
        ) as cursor:
            return self.single(cursor, 0)

    @DAO.check_success
    def add_item(self, item: ResourceType) -> int:
        with self._db.execute(
            "insert into resource_type (ResourceTypeName, IsProducible) "
            "values (%s, %s)",
            item.name, item.is_producible,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    @DAO.check_success
    def update_item(self, item: ResourceType):
        with self._db.execute(
            "update resource_type set ResourceTypeName=%s, IsProducible=%s "
            "where ResourceTypeId=%s",
            item.name, item.is_producible, item.id,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    def _delete_item(self, cursor, _id: int):
        cursor.execute(
            "delete from resource_type where ResourceTypeId = %s",
            (_id,)
        )
