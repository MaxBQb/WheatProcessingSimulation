from dataclasses import dataclass

from dao.base import DAO
from dao.items import ItemsDAO, ItemFilterOptions
from dao.live_query import live_query
from mappers import table_to_model
from model import Contract


@dataclass
class ContractFilterOptions(ItemFilterOptions):
    is_finished: bool = None
    is_violated: bool = None

    _NAME_FILTERS = [
        "LegalEntityName",
    ]

    def __post_init__(self):
        super().__post_init__()
        self._add_option("IsFinished = %s", self.is_finished)
        self._add_option("IsViolated = %s", self.is_violated)


class ContractsDAO(ItemsDAO[Contract]):
    @live_query
    def get_all(self, filter_options: ContractFilterOptions = None):
        where_clause, params = DAO.get_clause("WHERE", filter_options)
        with self._db.execute(
            f"SELECT * FROM view_contract contract" + where_clause,
            *params
        ) as cursor:
            return list(cursor)

    @live_query
    def get_item(self, _id: int) -> Contract:
        with self._db.execute("""
            SELECT * FROM contract 
            WHERE ContractId = %s""", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), Contract)

    @live_query
    def get_count(self) -> int:
        with self._db.execute(
            "SELECT COUNT(*) FROM contract"
        ) as cursor:
            return self.single(cursor, 0)

    @DAO.check_success
    def add_item(self, item: Contract):
        with self._db.cursor(commit_changes=True) as cursor:
            cursor.execute(
                "INSERT INTO contract (LegalEntityId, DeadlineTime, Price) "
                "VALUE (%s, %s, %s)",
                (item.legal_entity_id, item.deadline_time, item.price))
            item.id = cursor.lastrowid

            for resource in item.resources:
                cursor.execute("update resource set ContractId=%s "
                               "where ResourceId=%s", (item.id, resource))

            return item.id

    @DAO.check_success
    def update_item(self, item: Contract):
        with self._db.execute(
            "update contract set LegalEntityId=%s, IsFinished=%s, IsViolated=%s, Price=%s "
            "WHERE ContractId=%s",
            item.legal_entity_id, item.is_finished, item.is_violated, item.price, item.id,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    def _delete_item(self, cursor, _id: int):
        cursor.execute(
            "delete from contract where ContractId = %s",
            (_id,)
        )
