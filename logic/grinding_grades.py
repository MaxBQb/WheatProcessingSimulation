import inject

from dao.grinding_grades import GrindingGradesDAO, GrindingGradesFilterOptions
from logic.primitives import PrimitiveController
from model import GrindingGrade


class GrindingGradesController(PrimitiveController[GrindingGrade]):
    source = inject.attr(GrindingGradesDAO)
    filter_type = GrindingGradesFilterOptions
    HEADER = "помол отрубей"
