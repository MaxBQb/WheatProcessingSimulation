import PySimpleGUI as sg
import inject

import view.utils
from dao.machines import MachineFilterOptions
from logic.machines import MachinesController
from logic.table import Table
from model import Machine
from view import utils as utils, base as base
from view.items import ItemsView, AddItemView, T, EditItemView
from view.layout import machines_controls as control_panel_layout, machine_layout as layout
from view.update_handlers import update_listbox


class MachinesView(ItemsView[Machine]):
    title = view.utils.get_title("Промышленные механизмы")
    controller = inject.attr(MachinesController)

    LABEL_CURRENT_COUNT = "Текущее количество станков: {}"

    TABLE_HEADERS = ["Вид станка", "Включен"]

    def build_layout(self):
        super().build_layout()
        self.layout += control_panel_layout.get_layout()

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe_foreach(
            (
                control_panel_layout.checkbox_show_available,
                *control_panel_layout.radiobutton_show_powered.keys,
            ), self.on_filter_toggle
        )

    def on_filter_toggle(self, context: base.Context):
        options = MachineFilterOptions(
            control_panel_layout.radiobutton_show_powered.get_value(context.values),
            context.values[control_panel_layout.checkbox_show_available],
        )
        self.table_updater(self.controller.get_all(options))

    def table_value_to_str(self, value, column: int, row: int):
        return super().table_value_to_str(
            bool(value) if column == 2 else value,
            column,
            row
        )

    @base.transition
    def open_add_item_view(self):
        return AddMachineView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditMachineView(_id)


class AddMachineView(AddItemView[Machine]):
    title = utils.get_title("Добавление станка")
    controller = inject.attr(MachinesController)

    def __init__(self):
        super().__init__()
        self.item = Machine()
        self.machine_types = Table()

    def build_layout(self):
        self.layout = layout.get_layout()
        super().build_layout()

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(600, 300)
        ) | kwargs)

    def dynamic_build(self):
        super().dynamic_build()
        self.observe(
            layout.choice_list_type,
            self.controller.get_types(),
            self.update_types_list,
        )

    def update_types_list(self, element: sg.Listbox,
                          context: base.Context):
        self.machine_types: Table = context.value
        update_listbox(element, list(self.machine_types.column(1)))

    def build_item(self, context: base.Context) -> T:
        item, values = self.item, context.values

        row = utils.first(self.window[layout.choice_list_type].get_indexes(), None)
        item.type_id = self.machine_types.cell(0, row, None)

        item.is_powered = values[layout.checkbox_is_powered]
        return item


class EditMachineView(EditItemView[Machine], AddMachineView):
    title = utils.get_title("Изменение данных станка")
    controller = inject.attr(MachinesController)

    def __init__(self, _id: int):
        super().__init__(_id)
        self.__type_loaded = False

    def dynamic_build(self):
        super().dynamic_build()
        self.window[layout.checkbox_is_powered].update(self.item.is_powered)

    def update_types_list(self, element: sg.Listbox,
                          context: base.Context):
        super().update_types_list(element, context)
        if not self.__type_loaded:
            pos = list(self.machine_types.column(0)).index(self.item.type_id)
            element.update(set_to_index=pos, scroll_to_index=pos)
            self.__type_loaded = True
