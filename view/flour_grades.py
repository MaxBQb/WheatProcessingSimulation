import inject

import view.base as base
import view.utils
from logic.flour_grades import FlourGradesController
from model import FlourGrade
from view import utils as utils
from view.primitives import PrimitivesView, AddPrimitiveView, EditPrimitiveView


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


class AddFlourGradeView(AddPrimitiveView[FlourGrade]):
    title = utils.get_title("Добавление нового сорта муки")
    controller = inject.attr(FlourGradesController)

    def __init__(self):
        super().__init__()
        self.item = FlourGrade()


class EditFlourGradeView(EditPrimitiveView[FlourGrade], AddFlourGradeView):
    title = utils.get_title("Изменение названия сорта")
    controller = inject.attr(FlourGradesController)