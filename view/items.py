from abc import ABC, abstractmethod
from copy import deepcopy
from typing import TypeVar, Generic

import PySimpleGUI as sg

from logic.items import ItemsController
from logic.table import Table
from view import base as base
from view.confirmation import ConfirmDialogView
from view.layout import base_table_layout as layout, submit_button
from view.update_handlers import make_text_update_handler
from view.utils import auto_id

T = TypeVar('T')


class ItemsView(ABC, Generic[T], base.BaseInteractiveWindow):
    controller: ItemsController[T]

    LABEL_CURRENT_COUNT = "Текущее количество: {}"

    TABLE_HEADERS = ["Пусто"]

    def __init__(self):
        super().__init__()
        self.table_updater = None
        self.table_values = Table()

    def build_layout(self):
        self.layout = layout.get_layout(self.TABLE_HEADERS)

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
        self.table_updater = self.switchable_observe(
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

    def table_value_to_str(self, value, column: int, row: int):
        if value is None:
            return '—'
        if isinstance(value, bool):
            return "Да" if value else "Нет"
        return str(value)

    def update_table(self, table: sg.Table, context: base.Context):
        values = Table([
            [self.table_value_to_str(value, column_num, row_num)
             for column_num, value in enumerate(row)]
            for row_num, row in enumerate(context.value)
        ])
        selected = [
            list(values.column(0)).index(
                self.table_values.cell(0, selected_row)
            )
            for selected_row in table.SelectedRows
            if self.table_values.cell(0, selected_row, None) in values.column(0)
        ]
        self.table_values = values
        table.update(values=values.data, select_rows=selected)
        self.window[layout.button_delete].update(visible=False)
        self.window[layout.button_edit].update(visible=False)

    def on_item_selected(self, context: base.Context):
        self.window[layout.button_delete].update(visible=bool(len(context.value)))
        self.window[layout.button_edit].update(
            visible=len(context.value) == 1
        )


class AddItemView(ABC, Generic[T], base.BaseInteractiveWindow):
    controller: ItemsController[T]

    def __init__(self):
        super().__init__()
        self.item: T

    def build_layout(self):
        self.layout += [submit_button.get_layout()]

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe(
            submit_button.button_submit,
            self.on_submit
        )

    @abstractmethod
    def build_item(self, context: base.Context) -> T:
        pass

    def on_submit(self, context: base.Context):
        item = self.build_item(context)
        result = self.controller.add_item(item)
        if self.show_error(result):
            return
        self.close()


class EditItemView(Generic[T], AddItemView[T], ABC):
    def __init__(self, _id: int):
        super().__init__()
        self.item_livedata = self.controller.get_item(_id)
        self.item: T = self.item_livedata.value
        self.item_original: T = deepcopy(self.item)

    def dynamic_build(self):
        super().dynamic_build()
        self.item_livedata.observe(
            self.window,
            self.channel,
            self.on_item_updated,
            auto_id()
        )

    def on_item_updated(self, context: base.Context):
        if context.value is None:
            self.send_close_event()
        else:
            self.item_original = deepcopy(context.value)

    def on_submit(self, context: base.Context):
        item = self.build_item(context)
        if self.item_original == item:
            return
        result = self.controller.update_item(item)
        if self.show_error(result):
            return
        self.close()
