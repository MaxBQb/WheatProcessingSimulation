from datetime import datetime

import PySimpleGUI as sg
import inject

import view.utils
from dao.base import OptionalQuery
from dao.production_lines import ProductionLineFilterOptions
from logic.table import Table
from logic.production_lines import ProductionLinesController
from model import ProductionLine
from view import utils as utils, base as base
from view.items import ItemsView, AddItemView, T, EditItemView
from view.layout import production_lines_controls as control_panel_layout, production_line_layout as layout
from view.livedata import LiveData
from view.update_handlers import restrict_length, make_text_update_handler, update_listbox, update_listbox_advanced


class ProductionLinesView(ItemsView[ProductionLine]):
    title = view.utils.get_title("Производство")
    controller = inject.attr(ProductionLinesController)

    LABEL_CURRENT_COUNT = "Общее количество задач: {}"

    TABLE_HEADERS = ["Стандарт", "Затраченное время"]

    def build_layout(self):
        super().build_layout()
        self.layout += control_panel_layout.get_layout()

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(700, 500)
        ) | kwargs)

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe_foreach(
            (
                *control_panel_layout.radiobutton_show_finished.keys,
            ), self.on_filter_toggle
        )

    def table_value_to_str(self, value, column: int, row: int):
        if column == 2 and not value:
            return "В процессе"
        return super().table_value_to_str(value, column, row)

    def get_filter(self, context: base.Context) -> OptionalQuery:
        return self.controller.filter_type(
            self.get_search_query(context),
            control_panel_layout.radiobutton_show_finished.get_value(context.values),
        )

    @base.transition
    def open_add_item_view(self):
        return AddProductionLineView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditProductionLineView(_id)


class AddProductionLineView(AddItemView[ProductionLine]):
    title = utils.get_title("Старт производственной линии")
    controller = inject.attr(ProductionLinesController)
    _CREATION_MODE = True
    LABEL_START_DATE = "Дата начала: {}"
    LABEL_FINISH_DATE = "Дата окончания: {}"

    def __init__(self):
        super().__init__()
        self.item = ProductionLine()
        self.standards = Table()
        self.resources = Table()
        self.results = Table()
        self.workers = Table()
        self.machines = Table()

    def build_layout(self):
        self.layout = layout.get_layout(self._CREATION_MODE)
        super().build_layout()
        self.layout = layout.postprocess(self.layout)

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(800, 600)
        ) | kwargs)

    def set_handlers(self):
        super().set_handlers()
        self.set_creation_specific_listeners()

    def set_creation_specific_listeners(self):
        self.channel.subscribe(
            sg.TIMEOUT_KEY,
            self.update_start_time
        )

    def set_creation_specific_observers(self):
        self.observe(
            layout.choice_list_workers,
            self.controller.get_available_workers(),
            self.update_workers_list
        )
        self.observe(
            layout.choice_list_machines,
            self.controller.get_available_machines(),
            self.update_machines_list
        )
        self.observe(
            layout.choice_list_resources,
            self.controller.get_available_resources(),
            self.update_resources_list
        )
        self.observe(
            layout.choice_list_results,
            self.controller.get_results(),
            self.update_results_list
        )

    def update_start_time(self, context: base.Context):
        self.window[layout.label_start_time].update(
            self.LABEL_START_DATE.format(
                datetime.now().strftime(self.controller.date_format)
            )
        )

    def dynamic_build(self):
        super().dynamic_build()
        layout.on_finalized(self.window)
        self.observe(
            layout.choice_list_standard,
            self.controller.get_standards(),
            self.update_standards_list
        )
        self.set_creation_specific_observers()

    def update_standards_list(self, element: sg.Listbox, context: base.Context):
        self.standards = update_listbox_advanced(element, self.standards, context.value)

    def update_workers_list(self, element: sg.Listbox, context: base.Context):
        self.workers = update_listbox_advanced(element, self.workers, context.value)

    def update_machines_list(self, element: sg.Listbox, context: base.Context):
        self.machines = update_listbox_advanced(element, self.machines, context.value)

    def update_resources_list(self, element: sg.Listbox, context: base.Context):
        self.resources = update_listbox_advanced(element, self.resources, context.value)

    def update_results_list(self, element: sg.Listbox, context: base.Context):
        self.results = update_listbox_advanced(element, self.results, context.value)

    def build_item(self, context: base.Context) -> T:
        item, values = self.item, context.values

        item.standard_id = next(utils.get_selected(
            self.standards,
            self.window[layout.choice_list_standard].get_indexes()
        ), None)

        item.workers = list(utils.get_selected(
            self.workers,
            self.window[layout.choice_list_workers].get_indexes()
        ))

        item.machines = list(utils.get_selected(
            self.machines,
            self.window[layout.choice_list_machines].get_indexes()
        ))

        item.results = list(utils.get_selected(
            self.results,
            self.window[layout.choice_list_results].get_indexes()
        ))

        item.resources = list(utils.get_selected(
            self.resources,
            self.window[layout.choice_list_resources].get_indexes()
        ))

        return item


class EditProductionLineView(EditItemView[ProductionLine], AddProductionLineView):
    title = utils.get_title("Изменение данных сотрудника")
    controller = inject.attr(ProductionLinesController)
    _CREATION_MODE = False

    def __init__(self, _id: int):
        super().__init__(_id)
        self.__standard_loaded = False
        self.finish_time_livedata = LiveData(self.item.production_finish_time)

    def set_creation_specific_listeners(self):
        self.channel.subscribe(
            layout.button_finish,
            self.on_finish_pressed
        )
        self.channel.subscribe(
            layout.button_reset_finish,
            self.on_finish_reset_pressed
        )

    def on_finish_pressed(self, context: base.Context):
        self.finish_time_livedata.value = datetime.now()

    def on_finish_reset_pressed(self, context: base.Context):
        self.finish_time_livedata.value = None

    def set_creation_specific_observers(self):
        self.observe(
            layout.label_finish_time,
            self.finish_time_livedata,
            make_text_update_handler(
                lambda x: self.LABEL_FINISH_DATE.format(
                    x.strftime(self.controller.date_format)
                    if x else "Не окончено"
                )
            )
        )
        self.observe(
            layout.choice_list_workers,
            self.controller.get_used_workers(self.item),
            self.update_workers_list
        )
        self.observe(
            layout.choice_list_machines,
            self.controller.get_used_machines(self.item),
            self.update_machines_list
        )
        self.observe(
            layout.choice_list_resources,
            self.controller.get_used_resources(self.item),
            self.update_resources_list
        )
        self.observe(
            layout.choice_list_results,
            self.controller.get_produced_results(self.item),
            self.update_results_list
        )

    def dynamic_build(self):
        super().dynamic_build()
        if self.item.production_finish_time:
            self.window[layout.button_finish].update(visible=False)
            self.window[layout.button_reset_finish].update(visible=False)
        self.window[layout.label_start_time].update(
            self.LABEL_START_DATE.format(
                self.item.production_start_time
                    .strftime(self.controller.date_format)
            )
        )

    def update_standards_list(self, element: sg.Listbox,
                              context: base.Context):
        super().update_standards_list(element, context)
        if not self.__standard_loaded:
            pos = list(self.standards.column(0)).index(self.item.standard_id)
            element.update(set_to_index=pos, scroll_to_index=pos)
            self.__standard_loaded = True

    def build_item(self, context: base.Context) -> T:
        item, values = self.item, context.values

        item.standard_id = next(utils.get_selected(
            self.standards,
            self.window[layout.choice_list_standard].get_indexes()
        ), None)

        item.production_finish_time = self.finish_time_livedata.value
        return item
