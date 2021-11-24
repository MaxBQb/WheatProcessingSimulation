from dataclasses import dataclass

from dao.base import DAO
from dao.items import ItemsDAO, ItemFilterOptions
from dao.live_query import live_query
from mappers import table_to_model
from model import ProductionLine


@dataclass
class ProductionLineFilterOptions(ItemFilterOptions):
    is_finished: bool = None

    _NAME_FILTERS = [
        "StandardName",
    ]

    def __post_init__(self):
        super().__post_init__()
        self._add_option("(ProductionDuration is not null) = %s", self.is_finished)


class ProductionLinesDAO(ItemsDAO[ProductionLine]):
    @live_query
    def get_all(self, filter_options: ProductionLineFilterOptions = None):
        where_clause, params = DAO.get_clause("WHERE", filter_options)
        with self._db.execute(
            f"SELECT * FROM view_production_line production_line" + where_clause,
            *params
        ) as cursor:
            return list(cursor)

    @live_query
    def get_item(self, _id: int) -> ProductionLine:
        with self._db.execute("""
            SELECT * FROM production_line 
            WHERE ProductionLineId = %s""", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), ProductionLine)

    @live_query
    def get_count(self) -> int:
        with self._db.execute(
            "SELECT COUNT(*) FROM production_line"
        ) as cursor:
            return self.single(cursor, 0)

    @DAO.check_success
    def add_item(self, item: ProductionLine):
        with self._db.cursor(commit_changes=True) as cursor:
            cursor.execute("INSERT INTO production_line (StandardId) VALUE (%s)",
                           (item.standard_id,))
            item.id = cursor.lastrowid
            for result in item.results:
                cursor.execute("update resource set ParentProductionLineId=%s "
                               "where ResourceId=%s", (item.id, result))
            for resource in item.resources:
                cursor.execute("update resource set ProductionLineId=%s "
                               "where ResourceId=%s", (item.id, resource))
            for worker in item.workers:
                cursor.execute("insert into worker_to_production_line value (%s, %s)",
                               (item.id, worker))
            for machine in item.machines:
                cursor.execute("insert into machine_to_production_line value (%s, %s)",
                               (machine, item.id))
            return item.id

    @DAO.check_success
    def update_item(self, item: ProductionLine):
        with self._db.execute(
            "update production_line set StandardId=%s, ProductionFinishTime=%s "
            "where ProductionLineId=%s",
            item.standard_id, item.production_finish_time, item.id,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    def _delete_item(self, cursor, _id: int):
        cursor.execute(
            "delete from production_line where ProductionLineId = %s",
            (_id,)
        )
