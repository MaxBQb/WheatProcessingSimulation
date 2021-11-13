import PySimpleGUI as sg
import inject
import view.base as base
import view.utils
from logic.workers import WorkersController
from view.layout import base_table_layout as layout


class WorkersView(base.BaseInteractiveWindow):
    title = view.utils.get_title("Штат сотрудников")
    controller = inject.attr(WorkersController)

    def build_layout(self):
        self.layout = layout.get_layout([
            "ФИО", "Должность"
        ])

    def dynamic_build(self):
        super().dynamic_build()
        table: sg.Table = self.window[layout.table_entries]
        values = self.controller.get_table()
        values = [
            [str(val) for val in row]
            for row in values
        ]
        table.update(values=values)

    def set_handlers(self):
        super().set_handlers()
