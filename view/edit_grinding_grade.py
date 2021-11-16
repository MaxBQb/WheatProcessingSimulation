import inject

import view.utils as utils
from logic.grinding_grades import GrindingGradesController
from model import GrindingGrade
from view.add_grinding_grade import AddGrindingGradeView
from view.edit_primitive import EditPrimitiveView


class EditGrindingGradeView(EditPrimitiveView[GrindingGrade], AddGrindingGradeView):
    title = utils.get_title("Изменение названия помола")
    controller = inject.attr(GrindingGradesController)
