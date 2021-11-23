from dao.base import DAO
from dao.items import ItemsDAO
from dao.live_query import live_query
from mappers import table_to_model
from model import GrindingGrade


class GrindingGradesDAO(ItemsDAO[GrindingGrade]):
    @live_query
    def get_all(self, _=None):
        with self._db.execute(
            "SELECT * FROM grinding_grade"
        ) as cursor:
            return list(cursor)

    @live_query
    def get_item(self, _id: int) -> GrindingGrade:
        with self._db.execute(
            "SELECT * FROM grinding_grade "
            "WHERE GrindingGradeId = %s", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), GrindingGrade)

    @live_query
    def get_count(self) -> int:
        with self._db.execute(
            "SELECT COUNT(*) FROM grinding_grade"
        ) as cursor:
            return self.single(cursor, 0)

    @DAO.check_success
    def add_item(self, item: GrindingGrade) -> int:
        with self._db.execute(
            "insert into grinding_grade (GrindingGradeName) "
            "values (%s)", item.name,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    @DAO.check_success
    def update_item(self, item: GrindingGrade):
        with self._db.execute(
                "update grinding_grade set GrindingGradeName=%s "
                "where GrindingGradeId=%s",
                item.name, item.id,
                commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    def _delete_item(self, cursor, _id: int):
        cursor.execute(
            "delete from grinding_grade where GrindingGradeId = %s",
            (_id,)
        )
