import inject

import PySimpleGUI as sg
import view.base as base
import view.utils
from logic.workers import WorkersController
from model import Worker
from view.add_worker import AddWorkerView
from view.edit_worker import EditWorkerView
from view.items import ItemsView
from view.layout.base_table_layout import table_entries
from view.layout import workers_controls as control_panel_layout


class WorkersView(ItemsView[Worker]):
    title = view.utils.get_title("Штат сотрудников")
    controller = inject.attr(WorkersController)

    LABEL_CURRENT_COUNT = "Текущее количество сотрудников: {}"

    TABLE_HEADERS = ["ИО", "Должность", "Подчинённые"]

    def build_layout(self):
        super().build_layout()
        self.layout += control_panel_layout.get_layout()

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe(
            control_panel_layout.checkbox_show_available,
            self.on_filter_toggle
        )
        self.channel.subscribe(
            control_panel_layout.checkbox_show_chiefs,
            self.on_filter_toggle
        )

    def on_filter_toggle(self, context: base.Context):
        show_chiefs: bool = context.values[control_panel_layout.checkbox_show_chiefs]
        table: sg.Table = self.window[table_entries]
        self.table_updater(self.controller.get_all(
            show_chiefs,
            context.values[control_panel_layout.checkbox_show_available],
        ))

    @base.transition
    def open_add_item_view(self):
        return AddWorkerView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditWorkerView(_id)
