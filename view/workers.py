import PySimpleGUI as sg
import inject

import view.utils
from dao.base import OptionalQuery
from logic.table import Table
from logic.workers import WorkersController
from model import Worker
from view import utils as utils, base as base
from view.items import ItemsView, AddItemView, T, EditItemView
from view.layout import workers_controls as control_panel_layout, worker_layout as layout
from view.update_handlers import restrict_length, make_text_update_handler, update_listbox


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
        self.channel.subscribe_foreach(
            (
                control_panel_layout.checkbox_show_available,
                *control_panel_layout.radiobutton_show_chiefs.keys,
            ), self.on_filter_toggle
        )

    def get_filter(self, context: base.Context) -> OptionalQuery:
        return self.controller.filter_type(
            self.get_search_query(context),
            control_panel_layout.radiobutton_show_chiefs.get_value(context.values),
            context.values[control_panel_layout.checkbox_show_available],
        )

    @base.transition
    def open_add_item_view(self):
        return AddWorkerView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditWorkerView(_id)


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
            size=(600, 520)
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
        new_role_id = self.roles.cell(0, utils.first(context.element.get_indexes()), None)
        if self.item.role_id == new_role_id:
            return
        self.item.role_id = new_role_id
        self.chief_list_updater(self.controller.get_chief_candidates(self.item))

    def update_roles_list(self, element: sg.Listbox,
                          context: base.Context):
        selected = utils.get_new_selection(self.roles, context.value, element.get_indexes())
        self.roles: Table = context.value
        update_listbox(element, list(self.roles.column(1)), selected)

    def update_chief_candidates_list(self,
                                     element: sg.Listbox,
                                     context: base.Context):
        selected = utils.get_new_selection(self.workers, context.value, element.get_indexes())
        self.workers: Table = context.value
        update_listbox(element, list(self.workers.column(1)), selected)

    def build_item(self, context: base.Context) -> T:
        item, values = self.item, context.values
        item.name = utils.strip(values[layout.input_name])

        row = utils.first(self.window[layout.choice_list_role].get_indexes(), None)
        item.role_id = self.roles.cell(0, row, None)

        row = utils.first(self.window[layout.choice_list_chief].get_indexes(), 0)
        item.chief_id = self.workers.cell(0, row)
        return item


class EditWorkerView(EditItemView[Worker], AddWorkerView):
    title = utils.get_title("Изменение данных сотрудника")
    controller = inject.attr(WorkersController)

    def __init__(self, _id: int):
        super().__init__(_id)
        self.__role_loaded = False
        self.__chief_candidates_loaded = False

    def dynamic_build(self):
        super().dynamic_build()
        self.window[layout.input_name].update(self.item.name)

    def update_roles_list(self, element: sg.Listbox,
                          context: base.Context):
        super().update_roles_list(element, context)
        if not self.__role_loaded:
            pos = list(self.roles.column(0)).index(self.item.role_id)
            element.update(set_to_index=pos, scroll_to_index=pos)
            self.__role_loaded = True

    def update_chief_candidates_list(self,
                                     element: sg.Listbox,
                                     context: base.Context):
        super().update_chief_candidates_list(element, context)
        if not self.__chief_candidates_loaded:
            if self.item.chief_id is None:
                pos = 0
            else:
                pos = list(self.workers.column(0)).index(self.item.chief_id) + 1
            element.update(set_to_index=pos, scroll_to_index=pos)
            self.__chief_candidates_loaded = True
