import inject

import view.utils as utils
from logic.flour_grades import FlourGradesController
from model import FlourGrade
from view.add_primitives import AddPrimitiveView


class AddFlourGradeView(AddPrimitiveView[FlourGrade]):
    title = utils.get_title("Добавление нового сорта муки")
    controller = inject.attr(FlourGradesController)

    def __init__(self):
        super().__init__()
        self.item = FlourGrade()
