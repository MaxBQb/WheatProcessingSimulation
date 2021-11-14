import PySimpleGUI as sg
import inject
import view.base as base
import view.utils
from logic.workers import WorkersController
from view.layout import base_table_layout as layout
from view.update_handlers import make_text_update_handler


class WorkersView(base.BaseInteractiveWindow):
    title = view.utils.get_title("Штат сотрудников")
    controller = inject.attr(WorkersController)

    def build_layout(self):
        self.layout = layout.get_layout([
            "ФИО", "Должность"
        ])

    def dynamic_build(self):
        super().dynamic_build()
        self.observe(
            layout.table_entries,
            self.controller.get_table(),
            self.update_workers_table,
        )
        self.observe(
            layout.label_entries_count,
            self.controller.get_count(),
            make_text_update_handler("Текущее количество сотрудников: {}"),
        )

    def update_workers_table(self, table: sg.Table, context: base.Context):
        values = context.value
        values = [
            [str(val) for val in row]
            for row in values
        ]
        table.update(values=values)
