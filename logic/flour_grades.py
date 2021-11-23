import inject

from dao.flour_grades import FlourGradesDAO, FlourGradesFilterOptions
from logic.primitives import PrimitiveController
from model import FlourGrade


class FlourGradesController(PrimitiveController[FlourGrade]):
    source = inject.attr(FlourGradesDAO)
    filter_type = FlourGradesFilterOptions
    HEADER = "сорт муки"
