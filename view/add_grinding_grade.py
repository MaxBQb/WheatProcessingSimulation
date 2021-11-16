import inject

import view.utils as utils
from logic.grinding_grades import GrindingGradesController
from model import GrindingGrade
from view.add_primitives import AddPrimitiveView


class AddGrindingGradeView(AddPrimitiveView[GrindingGrade]):
    title = utils.get_title("Добавление нового помола отрубей")
    controller = inject.attr(GrindingGradesController)

    def __init__(self):
        super().__init__()
        self.item = GrindingGrade()
