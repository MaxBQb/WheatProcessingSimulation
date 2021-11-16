from abc import ABC, abstractmethod
from typing import TypeVar, Generic

import PySimpleGUI as sg

import view.base as base
from logic.items import ItemsController
from view.confirmation import ConfirmDialogView
from view.layout import base_table_layout as layout
from view.update_handlers import make_text_update_handler

T = TypeVar('T')


class ItemsView(ABC, Generic[T], base.BaseInteractiveWindow):
    controller: ItemsController[T]

    LABEL_CURRENT_COUNT = "Текущее количество: {}"

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
            lambda _: self.open_add_item_view()
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
            self.update_table,
        )
        self.observe(
            layout.label_entries_count,
            self.controller.get_count(),
            make_text_update_handler(self.LABEL_CURRENT_COUNT),
        )

    @abstractmethod
    @base.transition
    def open_add_item_view(self) \
            -> base.BaseInteractiveWindow:
        pass

    @abstractmethod
    @base.transition
    def open_edit_item_view(self, _id: int) \
            -> base.BaseInteractiveWindow:
        pass

    def on_edit(self, context: base.Context):
        table: sg.Table = self.window[layout.table_entries]
        if not len(table.SelectedRows):
            return
        _id = int(table.Values[table.SelectedRows[0]][0])
        self.open_edit_item_view(_id)

    def on_delete(self, context: base.Context):
        table: sg.Table = self.window[layout.table_entries]
        if not len(table.SelectedRows):
            return
        ids = [
            int(table.Values[i][0])
            for i in table.SelectedRows
        ]
        if not self.open_delete_confirmation(len(ids)):
            return
        self.show_error(self.controller.delete_items(*ids))

    @base.transition
    def open_delete_confirmation(self, count: int):
        return ConfirmDialogView(
            self.controller.get_delete_confirmation_text(count)
        )

    def update_table(self, table: sg.Table, context: base.Context):
        values = [
            [str(val) for val in row]
            for row in context.value
        ]
        table.update(values=values)
        self.window[layout.button_delete].update(visible=False)
        self.window[layout.button_edit].update(visible=False)

    def on_item_selected(self, context: base.Context):
        self.window[layout.button_delete].update(visible=True)
        self.window[layout.button_edit].update(
            visible=len(context.value) == 1
        )