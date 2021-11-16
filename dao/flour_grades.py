from dao.base import DAO
from dao.items import ItemsDAO
import dao.live_query
from mappers import table_to_model
from model import FlourGrade


live_query = dao.live_query.live_query(dao.live_query.tables.flour_grade)


class FlourGradesDAO(ItemsDAO[FlourGrade]):
    @live_query
    def get_all(self):
        with self._db.execute(
            "SELECT * FROM flour_grade"
        ) as cursor:
            return list(cursor)

    @live_query
    def get_item(self, _id: int) -> FlourGrade:
        with self._db.execute(
            "SELECT * FROM flour_grade "
            "WHERE FlourGradeId = %s", _id
        ) as cursor:
            return table_to_model(cursor.column_names, next(cursor, None), FlourGrade)

    @live_query
    def get_count(self) -> int:
        with self._db.execute(
            "SELECT COUNT(*) FROM flour_grade"
        ) as cursor:
            return self.single(cursor, 0)

    @DAO.check_success
    def add_item(self, item: FlourGrade) -> int:
        with self._db.execute(
            "insert into flour_grade (FlourGradeName) "
            "values (%s)", item.name,
            commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    @DAO.check_success
    def update_item(self, item: FlourGrade):
        with self._db.execute(
                "update flour_grade set FlourGradeName=%s "
                "where FlourGradeId=%s",
                item.name, item.id,
                commit_changes=True,
        ) as cursor:
            return cursor.lastrowid

    def _delete_item(self, cursor, _id: int):
        cursor.execute(
            "delete from flour_grade where FlourGradeId = %s",
            (_id,)
        )
