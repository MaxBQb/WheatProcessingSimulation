import inject

import view.utils as utils
from logic.flour_grades import FlourGradesController
from model import FlourGrade
from view.add_flour_grade import AddFlourGradeView
from view.edit_primitive import EditPrimitiveView


class EditFlourGradeView(EditPrimitiveView[FlourGrade], AddFlourGradeView):
    title = utils.get_title("Изменение названия сорта")
    controller = inject.attr(FlourGradesController)
