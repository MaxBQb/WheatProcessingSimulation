import inject

from dao.flour_grades import FlourGradesDAO
from logic.primitives import PrimitiveController
from model import FlourGrade


class FlourGradesController(PrimitiveController[FlourGrade]):
    source = inject.attr(FlourGradesDAO)
    HEADER = "сорт муки"
