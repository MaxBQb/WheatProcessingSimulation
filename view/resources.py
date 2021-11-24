import PySimpleGUI as sg
import inject

import view.utils
from dao.base import OptionalQuery
from logic.resources import ResourcesController
from logic.table import Table
from model import Resource
from view import utils as utils, base as base
from view.items import ItemsView, AddItemView, T, EditItemView
from view.layout import resources_controls as control_panel_layout, resource_layout as layout
from view.update_handlers import restrict_length, make_text_update_handler, update_listbox, update_listbox_advanced


class ResourcesView(ItemsView[Resource]):
    title = view.utils.get_title("Ресурсы и продукция")
    controller = inject.attr(ResourcesController)

    LABEL_CURRENT_COUNT = "Текущее количество хранимых партий: {}"

    TABLE_HEADERS = ["Вид ресурса", "Описание"]

    def build_layout(self):
        super().build_layout()
        self.layout += control_panel_layout.get_layout()

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe_foreach(
            (
                control_panel_layout.checkbox_show_available,
                control_panel_layout.checkbox_show_planned,
                *control_panel_layout.radiobutton_show_producible.keys,
            ), self.on_filter_toggle
        )

    def get_filter(self, context: base.Context) -> OptionalQuery:
        return self.controller.filter_type(
            self.get_search_query(context),
            control_panel_layout.radiobutton_show_producible.get_value(context.values),
            context.values[control_panel_layout.checkbox_show_available],
            context.values[control_panel_layout.checkbox_show_planned],
        )

    def table_value_to_str(self, value, column: int, row: int):
        if column == 2 and value:
            return value if not value else value[:60].split('\n')[0]
        return super().table_value_to_str(value, column, row)

    @base.transition
    def open_add_item_view(self):
        return AddResourceView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditResourceView(_id)


class AddResourceView(AddItemView[Resource]):
    title = utils.get_title("Добавление ресурса/продукта")
    controller = inject.attr(ResourcesController)

    def __init__(self):
        super().__init__()
        self.item = Resource()
        self.resource_types = Table()
        self.flour_grades = Table()
        self.grinding_grades = Table()

    def build_layout(self):
        self.layout = layout.get_layout()
        super().build_layout()

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(600, 600)
        ) | kwargs)

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe(
            layout.input_description,
            restrict_length(self.controller.description_max_len),
        )
        self.channel.subscribe(
            layout.choice_list_type,
            self.on_resource_type_selected
        )

    def dynamic_build(self):
        super().dynamic_build()
        layout.on_finalized(self.window)
        self.observe(
            layout.choice_list_type,
            self.controller.get_resource_types(),
            self.update_resource_types_list,
        )
        self.observe(
            layout.choice_list_flour_grade,
            self.controller.get_flour_grades(),
            self.update_flour_grades_list,
        )
        self.observe(
            layout.choice_list_grinding_grade,
            self.controller.get_grinding_grades(),
            self.update_grinding_grades_list,
        )

    def on_resource_type_selected(self, context: base.Context):
        resource_type = self.resource_types.cell(0, utils.first(context.element.get_indexes()), None)
        self.update_sections_visibility(resource_type)

    def update_sections_visibility(self, resource_type_id: int):
        ids = [
            layout.section_wheat,
            layout.section_bran,
            layout.section_flour,
            layout.section_description,
        ]
        _id = ids[min(resource_type_id, 4)-1]
        for each in ids:
            self.window[each].update(visible=False)
        self.window[_id].update(visible=True)

    def update_resource_types_list(self, element: sg.Listbox, context: base.Context):
        self.resource_types = update_listbox_advanced(element, self.resource_types, context.value)

    def update_flour_grades_list(self, element: sg.Listbox, context: base.Context):
        self.flour_grades = update_listbox_advanced(element, self.flour_grades, context.value)

    def update_grinding_grades_list(self, element: sg.Listbox, context: base.Context):
        self.grinding_grades = update_listbox_advanced(element, self.grinding_grades, context.value)

    def build_item(self, context: base.Context) -> T:
        item, values = self.item, context.values
        item.description = utils.strip(values[layout.input_description])

        row = utils.first(self.window[layout.choice_list_type].get_indexes(), None)
        item.type_id = self.resource_types.cell(0, row, None)

        row = utils.first(self.window[layout.choice_list_flour_grade].get_indexes(), None)
        item.flour_grade_id = self.flour_grades.cell(0, row, None)

        row = utils.first(self.window[layout.choice_list_grinding_grade].get_indexes(), None)
        item.grinding_grade_id = self.grinding_grades.cell(0, row, None)

        item.vitreousness = values.get(layout.slider_vitreousness, None)
        item.contamination = values.get(layout.slider_vitreousness, None)
        return item


class EditResourceView(EditItemView[Resource], AddResourceView):
    title = utils.get_title("Изменение данных ресурса/продукта")
    controller = inject.attr(ResourcesController)

    def __init__(self, _id: int):
        super().__init__(_id)
        self.__type_loaded = False
        self.__flour_grade_loaded = False
        self.__grinding_grade_loaded = False

    def dynamic_build(self):
        self.update_sections_visibility(self.item.type_id)
        super().dynamic_build()
        if self.item.description:
            self.window[layout.input_description].update(self.item.description)

        if self.item.vitreousness:
            self.window[layout.slider_vitreousness].update(self.item.vitreousness)

        if self.item.contamination:
            self.window[layout.slider_contamination].update(self.item.contamination)

    def update_resource_types_list(self, element: sg.Listbox, context: base.Context):
        super().update_resource_types_list(element, context)
        if not self.__type_loaded:
            pos = list(self.resource_types.column(0)).index(self.item.type_id)
            element.update(set_to_index=pos, scroll_to_index=pos)
            self.__type_loaded = True

    def update_flour_grades_list(self, element: sg.Listbox, context: base.Context):
        super().update_flour_grades_list(element, context)
        if not self.__flour_grade_loaded:
            if self.item.flour_grade_id:
                pos = list(self.flour_grades.column(0)).index(self.item.flour_grade_id)
                element.update(set_to_index=pos, scroll_to_index=pos)
            self.__flour_grade_loaded = True

    def update_grinding_grades_list(self, element: sg.Listbox, context: base.Context):
        super().update_grinding_grades_list(element, context)
        if not self.__grinding_grade_loaded:
            if self.item.grinding_grade_id:
                pos = list(self.grinding_grades.column(0)).index(self.item.grinding_grade_id)
                element.update(set_to_index=pos, scroll_to_index=pos)
            self.__grinding_grade_loaded = True
