from dao.base import DAO
from dao.items import ItemsDAO, ItemFilterOptions
from dao.live_query import live_query
from mappers import table_to_model
from model import LegalEntity


class LegalEntitiesFilterOptions(ItemFilterOptions):
    _NAME_FILTERS = [
        "LegalEntityName",
        "Address",
        "ContactPhone",
    ]


class LegalEntitiesDAO(ItemsDAO[LegalEntity]):
    @live_query
    def get_all(self, filter_options: LegalEntitiesFilterOptions = None):
        where_clause, params = DAO.get_clause("WHERE", filter_options)
        with self._db.execute(
            "SELECT * FROM view_legal_entity legal_entity " + where_clause,
            *params
        ) as cursor:
            return list(cursor)

    @live_query
    def get_item(self, _id: int) -> LegalEntity:
        with self._db.execute(
            "SELECT * FROM legal_entity "
            "WHERE LegalEntityId = %s", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), LegalEntity)

    @live_query
    def get_count(self) -> int:
        with self._db.execute(
            "SELECT COUNT(*) FROM legal_entity"
        ) as cursor:
            return self.single(cursor, 0)

    @DAO.check_success
    def add_item(self, item: LegalEntity) -> int:
        with self._db.execute(
            "insert into legal_entity (ContactPhone, Address, LegalEntityName)"
            "values (%s, %s, %s)",
            item.contact_phone, item.address, item.name,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    @DAO.check_success
    def update_item(self, item: LegalEntity):
        with self._db.execute(
            "update legal_entity set ContactPhone=%s, Address=%s, LegalEntityName=%s "
            "where LegalEntityId=%s",
            item.contact_phone, item.address, item.name, item.id,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    def _delete_item(self, cursor, _id: int):
        cursor.execute(
            "delete from legal_entity where LegalEntityId = %s",
            (_id,)
        )
