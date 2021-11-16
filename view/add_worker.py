import PySimpleGUI as sg
import inject

import view.base as base
import view.utils as utils
from logic.table import Table
from logic.workers import WorkersController
from model import Worker
from view.add_item import AddItemView, T
from view.layout import worker_layout as layout
from view.update_handlers import update_listbox, restrict_length, make_text_update_handler


class AddWorkerView(AddItemView[Worker]):
    title = utils.get_title("Добавление сотрудника")
    controller = inject.attr(WorkersController)

    def __init__(self):
        super().__init__()
        self.item = Worker()
        self.roles = Table()
        self.workers = Table()
        self.chief_list_updater = None

    def build_layout(self):
        self.layout = layout.get_layout()
        super().build_layout()

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(600, 500)
        ) | kwargs)

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe(
            layout.choice_list_role,
            self.on_role_selected
        )
        self.channel.subscribe(
            layout.input_name,
            restrict_length(self.controller.name_max_len),
            base.with_element(
                make_text_update_handler(lambda x: x.title())
            )
        )

    def dynamic_build(self):
        super().dynamic_build()
        layout.on_finalized(self.window)
        self.observe(
            layout.choice_list_role,
            self.controller.get_roles(),
            self.update_roles_list,
        )
        self.chief_list_updater = self.switchable_observe(
            layout.choice_list_chief,
            self.controller.get_chief_candidates(self.item),
            self.update_chief_candidates_list,
        )

    def on_role_selected(self, context: base.Context):
        self.item.role_id = self.roles.cell(0, utils.first(context.element.get_indexes()), None)
        self.chief_list_updater(self.controller.get_chief_candidates(self.item))

    def update_roles_list(self, element: sg.Listbox,
                          context: base.Context):
        self.roles: Table = context.value
        update_listbox(element, list(self.roles.column(1)))

    def update_chief_candidates_list(self,
                                     element: sg.Listbox,
                                     context: base.Context):
        self.workers: Table = context.value
        update_listbox(element, list(self.workers.column(1)))

    def build_item(self, context: base.Context) -> T:
        item, values = self.item, context.values
        item.name = values[layout.input_name]

        row = utils.first(self.window[layout.choice_list_role].get_indexes(), None)
        item.role_id = self.roles.cell(0, row, None)

        row = utils.first(self.window[layout.choice_list_chief].get_indexes(), 0)
        item.chief_id = self.workers.cell(0, row)
        return item
