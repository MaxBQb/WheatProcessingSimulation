import inject

import view.base as base
import view.utils
from logic.flour_grades import FlourGradesController
from model import FlourGrade
from view.add_flour_grade import AddFlourGradeView
from view.edit_flour_grade import EditFlourGradeView
from view.primitives import PrimitivesView


class FlourGradesView(PrimitivesView[FlourGrade]):
    title = view.utils.get_title("Сорта муки")
    controller = inject.attr(FlourGradesController)

    LABEL_CURRENT_COUNT = "Текущее количество сортов: {}"

    @base.transition
    def open_add_item_view(self):
        return AddFlourGradeView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditFlourGradeView(_id)
