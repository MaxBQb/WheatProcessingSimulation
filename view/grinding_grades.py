import inject

import view.base as base
import view.utils
from logic.grinding_grades import GrindingGradesController
from model import GrindingGrade
from view import utils as utils
from view.primitives import PrimitivesView, AddPrimitiveView, EditPrimitiveView


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


class AddGrindingGradeView(AddPrimitiveView[GrindingGrade]):
    title = utils.get_title("Добавление нового помола отрубей")
    controller = inject.attr(GrindingGradesController)

    def __init__(self):
        super().__init__()
        self.item = GrindingGrade()


class EditGrindingGradeView(EditPrimitiveView[GrindingGrade], AddGrindingGradeView):
    title = utils.get_title("Изменение названия помола")
    controller = inject.attr(GrindingGradesController)