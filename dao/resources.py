from dataclasses import dataclass

from dao.base import DAO
from dao.items import ItemsDAO, ItemFilterOptions
from dao.live_query import live_query
from mappers import table_to_model
from model import Resource


@dataclass
class ResourceFilterOptions(ItemFilterOptions):
    is_producible: bool = None
    is_available: bool = False
    is_planned: bool = False

    _NAME_FILTERS = [
        "ResourceTypeName",
        "Comment",
    ]

    def __post_init__(self):
        super().__post_init__()
        self._add_toggle("IsAvailable = 1", self.is_available)
        self._add_toggle("IsPlanned = 1", self.is_planned)
        self._add_option("IsProducible = %s", self.is_producible)


class ResourcesDAO(ItemsDAO[Resource]):
    @live_query
    def get_all(self, filter_options: ResourceFilterOptions = None):
        where_clause, params = DAO.get_clause("WHERE", filter_options)
        with self._db.execute(
                f"SELECT ResourceId, ResourceTypeName, Comment FROM view_resource resource" + where_clause,
                *params
        ) as cursor:
            return list(cursor)

    @live_query
    def get_item(self, _id: int) -> Resource:
        with self._db.execute(
                "SELECT * FROM resource "
                "WHERE ResourceId = %s", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), Resource)

    @live_query
    def get_results_by_production_line(self, _id: int):
        with self._db.execute("""
            SELECT r.ResourceId, ResourceTypeName, Comment FROM production_line 
            INNER JOIN resource r on production_line.ProductionLineId = r.ParentProductionLineId
            INNER JOIN view_resource vr on r.ResourceId = vr.ResourceId
            WHERE production_line.ProductionLineId = %s
        """, _id) as cursor:
            return list(cursor)

    @live_query
    def get_products_by_contract(self, _id: int):
        with self._db.execute("""
            SELECT r.ResourceId, ResourceTypeName, Comment FROM contract 
            INNER JOIN resource r on contract.ContractId = r.ContractId
            INNER JOIN view_resource vr on r.ResourceId = vr.ResourceId
            WHERE contract.ContractId = %s
        """, _id) as cursor:
            return list(cursor)

    @live_query
    def get_resources_by_production_line(self, _id: int):
        with self._db.execute("""
            SELECT r.ResourceId, ResourceTypeName, Comment FROM production_line 
            INNER JOIN resource r on production_line.ProductionLineId = r.ProductionLineId
            INNER JOIN view_resource vr on r.ResourceId = vr.ResourceId
            WHERE production_line.ProductionLineId = %s
        """, _id) as cursor:
            return list(cursor)

    @live_query
    def get_count(self) -> int:
        with self._db.execute(
                "SELECT COUNT(*) FROM resource"
        ) as cursor:
            return self.single(cursor, 0)

    @DAO.check_success
    def add_item(self, item: Resource) -> int:
        with self._db.execute("""
            insert into resource (
                ResourceTypeId, Description, FlourGradeId,
                Vitreousness, Contamination, GrindingGradeId
            ) values (%s, %s, %s, %s, %s, %s)""",
                              item.type_id, item.description, item.flour_grade_id,
                              item.vitreousness, item.contamination, item.grinding_grade_id,
                              commit_changes=True,
                              ) as cursor:
            return cursor.lastrowid

    @DAO.check_success
    def update_item(self, item: Resource):
        with self._db.execute("""
            update resource set 
            ResourceTypeId=%s, Description=%s, FlourGradeId=%s,
            Vitreousness=%s, Contamination=%s, GrindingGradeId=%s 
            where ResourceId=%s""",
            item.type_id, item.description, item.flour_grade_id,
            item.vitreousness, item.contamination, item.grinding_grade_id,
            item.id, commit_changes=True
        ) as cursor:
            return cursor.lastrowid

    def _delete_item(self, cursor, _id: int):
        cursor.execute(
            "delete from resource where ResourceId = %s",
            (_id,)
        )
