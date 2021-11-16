import PySimpleGUI as sg
import inject

import view.base as base
import view.utils
from logic.workers import WorkersController
from view.add_worker import AddWorkerView
from view.confirmation import ConfirmDialogView
from view.edit_worker import EditWorkerView
from view.layout import base_table_layout as layout
from view.update_handlers import make_text_update_handler


class WorkersView(base.BaseInteractiveWindow):
    title = view.utils.get_title("Штат сотрудников")
    controller = inject.attr(WorkersController)

    def build_layout(self):
        self.layout = layout.get_layout([
            "ИО", "Должность"
        ])

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe(
            layout.table_entries,
            self.on_item_selected
        )
        self.channel.subscribe(
            layout.button_add,
            lambda _: self._open_dependent_window(AddWorkerView())
        )
        self.channel.subscribe(
            layout.button_edit,
            self.on_edit
        )
        self.channel.subscribe(
            layout.button_delete,
            self.on_delete
        )

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(800, 600)
        ) | kwargs)

    def dynamic_build(self):
        super().dynamic_build()
        self.observe(
            layout.table_entries,
            self.controller.get_all(),
            self.update_workers_table,
        )
        self.observe(
            layout.label_entries_count,
            self.controller.get_count(),
            make_text_update_handler("Текущее количество сотрудников: {}"),
        )

    def on_edit(self, context: base.Context):
        table: sg.Table = self.window[layout.table_entries]
        _id = int(table.Values[table.SelectedRows[0]][0])
        self._open_dependent_window(EditWorkerView(_id))

    def on_delete(self, context: base.Context):
        table: sg.Table = self.window[layout.table_entries]
        ids = [
            int(table.Values[i][0])
            for i in table.SelectedRows
        ]
        if not self._open_dependent_window(ConfirmDialogView(
            "Вы точно хотите произвести удаление?\n" +
            f"Всего удалений: {len(ids)}"
        )):
            return
        self.show_error(self.controller.delete_workers(*ids))

    def update_workers_table(self, table: sg.Table, context: base.Context):
        values = [
            [str(val) for val in row]
            for row in context.value
        ]
        table.update(values=values)

    def on_item_selected(self, context: base.Context):
        self.window[layout.button_delete].update(visible=True)
        self.window[layout.button_edit].update(
            visible=len(context.value) == 1
        )
