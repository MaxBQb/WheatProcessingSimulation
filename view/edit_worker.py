import PySimpleGUI as sg
import inject

import view.base as base
import view.utils as utils
from logic.workers import WorkersController
from model import Worker
from view.add_worker import AddWorkerView
from view.layout import worker_layout as layout


class EditWorkerView(AddWorkerView):
    title = utils.get_title("Изменение данных сотрудника")
    controller = inject.attr(WorkersController)

    def __init__(self, _id: int):
        super().__init__()
        self.worker = self.controller.get_worker(_id).value
        self.worker_original = Worker(**self.worker.__dict__)
        self.__role_loaded = False
        self.__chief_candidates_loaded = False

    def dynamic_build(self):
        super().dynamic_build()
        self.window[layout.input_name].update(self.worker.name)

    def update_roles_list(self, element: sg.Listbox,
                          context: base.Context):
        super().update_roles_list(element, context)
        if not self.__role_loaded:
            pos = list(self.roles.values()).index(self.worker.role_id)
            element.update(set_to_index=pos, scroll_to_index=pos)
            self.__role_loaded = True

    def update_chief_candidates_list(self,
                                     element: sg.Listbox,
                                     context: base.Context):
        super().update_chief_candidates_list(element, context)
        if not self.__chief_candidates_loaded:
            if self.worker.chief_id is None:
                pos = 0
            else:
                pos = list(self.workers.values()).index(self.worker.chief_id)+1
            element.update(set_to_index=pos, scroll_to_index=pos)
            self.__role_loaded = True

    def send_worker(self, worker: Worker):
        if self.worker_original == worker:
            return
        return self.controller.update_worker(worker)
