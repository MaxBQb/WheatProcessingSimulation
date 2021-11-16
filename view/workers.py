import inject

import view.base as base
import view.utils
from logic.workers import WorkersController
from model import Worker
from view.add_worker import AddWorkerView
from view.edit_worker import EditWorkerView
from view.items import ItemsView


class WorkersView(ItemsView[Worker]):
    title = view.utils.get_title("Штат сотрудников")
    controller = inject.attr(WorkersController)

    LABEL_CURRENT_COUNT = "Текущее количество сотрудников: {}"

    @base.transition
    def open_add_item_view(self):
        return AddWorkerView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditWorkerView(_id)
