from contextlib import suppress
from datetime import datetime

import PySimpleGUI as sg
import inject

import view.utils
from dao.base import OptionalQuery
from logic.contracts import ContractsController
from logic.table import Table
from model import Contract
from view import utils as utils, base as base
from view.items import ItemsView, AddItemView, T, EditItemView
from view.layout import contracts_controls as control_panel_layout, contract_layout as layout
from view.livedata import LiveData
from view.update_handlers import make_text_update_handler, update_listbox_advanced


class ContractsView(ItemsView[Contract]):
    title = view.utils.get_title("Договора")
    controller = inject.attr(ContractsController)

    LABEL_CURRENT_COUNT = "Текущее количество договоров: {}"

    TABLE_HEADERS = ["Юр. лицо", "Дата подписания", "Крайний срок исполнения"]

    def build_layout(self):
        super().build_layout()
        self.layout += control_panel_layout.get_layout()

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(900, 600)
        ) | kwargs)

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe_foreach(
            (
                *control_panel_layout.radiobutton_show_finished.keys,
                *control_panel_layout.radiobutton_show_violated.keys,
            ), self.on_filter_toggle
        )

    def table_value_to_str(self, value, column: int, row: int):
        if column in (2, 3):
            return value.strftime(self.controller.date_format)
        return super().table_value_to_str(value, column, row)

    def get_filter(self, context: base.Context) -> OptionalQuery:
        return self.controller.filter_type(
            self.get_search_query(context),
            control_panel_layout.radiobutton_show_finished.get_value(context.values),
            control_panel_layout.radiobutton_show_violated.get_value(context.values),
        )

    @base.transition
    def open_add_item_view(self):
        return AddContractView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditContractView(_id)


class AddContractView(AddItemView[Contract]):
    title = utils.get_title("Создание договора")
    controller = inject.attr(ContractsController)
    _CREATION_MODE = True
    LABEL_START_DATE = "Дата подписания: {}"
    LABEL_FINISH_DATE = "Крайняя дата завершения: {}"

    def __init__(self):
        super().__init__()
        self.item = Contract()
        self.legal_entities = Table()
        self.resources = Table()

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
            layout.choice_list_resources,
            self.controller.get_available_products(),
            self.update_resources_list
        )

    def update_start_time(self, context: base.Context):
        self.window[layout.label_creation_time].update(
            self.LABEL_START_DATE.format(
                datetime.now().strftime(self.controller.date_format)
            )
        )

    def dynamic_build(self):
        super().dynamic_build()
        layout.on_finalized(self.window)
        self.observe(
            layout.choice_list_legal_entity,
            self.controller.get_legal_entities(),
            self.update_legal_entities_list
        )
        self.set_creation_specific_observers()

    def update_legal_entities_list(self, element: sg.Listbox, context: base.Context):
        self.legal_entities = update_listbox_advanced(element, self.legal_entities, context.value)

    def update_resources_list(self, element: sg.Listbox, context: base.Context):
        self.resources = update_listbox_advanced(element, self.resources, context.value)

    def build_item(self, context: base.Context) -> T:
        item, values = self.item, context.values

        item.legal_entity_id = next(utils.get_selected(
            self.legal_entities,
            self.window[layout.choice_list_legal_entity].get_indexes()
        ), None)

        item.resources = list(utils.get_selected(
            self.resources,
            self.window[layout.choice_list_resources].get_indexes()
        ))

        with suppress(ValueError):
            item.price = float(values[layout.input_price])

        return item


class EditContractView(EditItemView[Contract], AddContractView):
    title = utils.get_title("Изменение данных договора")
    controller = inject.attr(ContractsController)
    _CREATION_MODE = False

    def __init__(self, _id: int):
        super().__init__(_id)
        self.__legal_entity_loaded = False

    def set_creation_specific_listeners(self):
        pass

    def set_creation_specific_observers(self):
        self.observe(
            layout.choice_list_resources,
            self.controller.get_used_products(self.item),
            self.update_resources_list
        )

    def dynamic_build(self):
        super().dynamic_build()
        if not self.item.is_finished:
            self.window[layout.checkbox_is_finished].update(visible=True)
        self.window[layout.label_creation_time].update(
            self.LABEL_START_DATE.format(
                self.item.creation_time.strftime(
                    self.controller.date_format
                )
            )
        )
        self.window[layout.label_deadline_time].update(
            self.LABEL_FINISH_DATE.format(
                self.item.deadline_time.strftime(
                    self.controller.date_format
                )
            )
        )
        self.window[layout.input_price].update(self.item.price)

    def update_legal_entities_list(self, element: sg.Listbox,
                                   context: base.Context):
        super().update_legal_entities_list(element, context)
        if not self.__legal_entity_loaded:
            pos = list(self.legal_entities.column(0)).index(self.item.legal_entity_id)
            element.update(set_to_index=pos, scroll_to_index=pos)
            self.__legal_entity_loaded = True

    def build_item(self, context: base.Context) -> T:
        item, values = self.item, context.values

        item.legal_entity_id = next(utils.get_selected(
            self.legal_entities,
            self.window[layout.choice_list_legal_entity].get_indexes()
        ), None)

        if not item.is_finished:
            item.is_finished = values[layout.checkbox_is_finished]

        with suppress(ValueError):
            item.price = float(values[layout.input_price])

        return item
