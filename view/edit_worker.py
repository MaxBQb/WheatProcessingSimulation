import PySimpleGUI as sg
import inject

import view.base as base
import view.utils as utils
from logic.workers import WorkersController
from model import Worker
from view.add_worker import AddWorkerView
from view.edit_item import EditItemView
from view.layout import worker_layout as layout


class EditWorkerView(EditItemView[Worker], AddWorkerView):
    title = utils.get_title("Изменение данных сотрудника")
    controller = inject.attr(WorkersController)

    def __init__(self, _id: int):
        super().__init__(_id)
        self.__role_loaded = False
        self.__chief_candidates_loaded = False

    def dynamic_build(self):
        super().dynamic_build()
        self.window[layout.input_name].update(self.item.name)

    def update_roles_list(self, element: sg.Listbox,
                          context: base.Context):
        super().update_roles_list(element, context)
        if not self.__role_loaded:
            pos = list(self.roles.column(0)).index(self.item.role_id)
            element.update(set_to_index=pos, scroll_to_index=pos)
            self.__role_loaded = True

    def update_chief_candidates_list(self,
                                     element: sg.Listbox,
                                     context: base.Context):
        super().update_chief_candidates_list(element, context)
        if not self.__chief_candidates_loaded:
            if self.item.chief_id is None:
                pos = 0
            else:
                pos = list(self.workers.column(0)).index(self.item.chief_id) + 1
            element.update(set_to_index=pos, scroll_to_index=pos)
            self.__role_loaded = True
