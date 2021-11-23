import PySimpleGUI as sg
import inject

import view.utils
from logic.table import Table
from logic.standards import StandardsController
from model import Standard
from view import utils as utils, base as base
from view.items import ItemsView, AddItemView, T, EditItemView
from view.layout import standard_layout as layout
from view.update_handlers import restrict_length, make_text_update_handler, update_listbox


class StandardsView(ItemsView[Standard]):
    title = view.utils.get_title("Стандарты производства")
    controller = inject.attr(StandardsController)

    LABEL_CURRENT_COUNT = "Текущее количество стандартов: {}"

    TABLE_HEADERS = ["Название", "Описание"]

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(1000, 400)
        ) | kwargs)

    def table_value_to_str(self, value, column: int, row: int):
        if column == 2 and value:
            return value if not value else value[:60].split('\n')[0]
        return super().table_value_to_str(value, column, row)

    @base.transition
    def open_add_item_view(self):
        return AddStandardView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditStandardView(_id)


class AddStandardView(AddItemView[Standard]):
    title = utils.get_title("Добавление нового стандарта/рецепта")
    controller = inject.attr(StandardsController)

    def __init__(self):
        super().__init__()
        self.item = Standard()

    def build_layout(self):
        self.layout = layout.get_layout()
        super().build_layout()

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(600, 440)
        ) | kwargs)

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe(
            layout.input_name,
            restrict_length(self.controller.name_max_len),
            base.with_element(
                make_text_update_handler(lambda x: x.title())
            )
        )
        self.channel.subscribe(
            layout.input_description,
            restrict_length(self.controller.description_max_len),
        )

    def dynamic_build(self):
        super().dynamic_build()
        layout.on_finalized(self.window)

    def build_item(self, context: base.Context) -> T:
        item, values = self.item, context.values
        item.name = utils.strip(values[layout.input_name])
        item.description = utils.strip(values[layout.input_description])
        return item


class EditStandardView(EditItemView[Standard], AddStandardView):
    title = utils.get_title("Изменение стандарта")
    controller = inject.attr(StandardsController)

    def dynamic_build(self):
        super().dynamic_build()
        self.window[layout.input_name].update(self.item.name)
        self.window[layout.input_description].update(self.item.description)
