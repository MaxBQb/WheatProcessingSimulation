from dao.base import DAO
from dao.items import ItemsDAO, ItemFilterOptions
from dao.live_query import live_query
from mappers import table_to_model
from model import Standard


class StandardsFilterOptions(ItemFilterOptions):
    _NAME_FILTERS = [
        "StandardName",
        "StandardDescription",
    ]


class StandardsDAO(ItemsDAO[Standard]):
    @live_query
    def get_all(self, filter_options: StandardsFilterOptions = None):
        where_clause, params = DAO.get_clause("WHERE", filter_options)
        with self._db.execute(
            "SELECT * FROM standard " + where_clause,
            *params
        ) as cursor:
            return list(cursor)

    @live_query
    def get_item(self, _id: int) -> Standard:
        with self._db.execute(
            "SELECT * FROM standard "
            "WHERE StandardId = %s", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), Standard)

    @live_query
    def get_count(self) -> int:
        with self._db.execute(
            "SELECT COUNT(*) FROM standard"
        ) as cursor:
            return self.single(cursor, 0)

    @DAO.check_success
    def add_item(self, item: Standard) -> int:
        with self._db.execute(
            "insert into standard (StandardName, StandardDescription)"
            "values (%s, %s)",
            item.name, item.description,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    @DAO.check_success
    def update_item(self, item: Standard):
        with self._db.execute(
            "update standard set StandardName=%s, StandardDescription=%s "
            "where StandardId=%s",
            item.name, item.description, item.id,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    def _delete_item(self, cursor, _id: int):
        cursor.execute(
            "delete from standard where StandardId = %s",
            (_id,)
        )
