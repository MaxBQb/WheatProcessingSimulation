import inject

from dao.grinding_grades import GrindingGradesDAO
from logic.primitives import PrimitiveController
from model import GrindingGrade


class GrindingGradesController(PrimitiveController[GrindingGrade]):
    source = inject.attr(GrindingGradesDAO)
    HEADER = "помол отрубей"
