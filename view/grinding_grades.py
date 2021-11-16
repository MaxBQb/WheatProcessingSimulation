import inject

import view.base as base
import view.utils
from logic.grinding_grades import GrindingGradesController
from model import GrindingGrade
from view.add_grinding_grade import AddGrindingGradeView
from view.edit_grinding_grade import EditGrindingGradeView
from view.primitives import PrimitivesView


class GrindingGradesView(PrimitivesView[GrindingGrade]):
    title = view.utils.get_title("Степень помола отрубей")
    controller = inject.attr(GrindingGradesController)

    LABEL_CURRENT_COUNT = "Текущее количество помолов: {}"

    @base.transition
    def open_add_item_view(self):
        return AddGrindingGradeView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditGrindingGradeView(_id)
