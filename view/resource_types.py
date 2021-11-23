import inject

import view.utils
from logic.resource_types import ResourceTypesController
from model import ResourceType
from view import utils as utils, base as base
from view.items import ItemsView, AddItemView, T, EditItemView
from view.layout import resource_type_layout as layout
from view.update_handlers import restrict_length, make_text_update_handler


class ResourceTypesView(ItemsView[ResourceType]):
    title = view.utils.get_title("Типы ресурсов")
    controller = inject.attr(ResourceTypesController)

    LABEL_CURRENT_COUNT = "Текущее количество типов: {}"

    TABLE_HEADERS = ["Название типа", "На продажу"]

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(600, 400)
        ) | kwargs)

    def table_value_to_str(self, value, column: int, row: int):
        return super().table_value_to_str(
            bool(value) if column == 2 else value,
            column,
            row
        )

    @base.transition
    def open_add_item_view(self):
        return AddResourceTypeView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditResourceTypeView(_id)


class AddResourceTypeView(AddItemView[ResourceType]):
    title = utils.get_title("Добавление типа ресурса")
    controller = inject.attr(ResourceTypesController)

    def __init__(self):
        super().__init__()
        self.item = ResourceType()

    def build_layout(self):
        self.layout = layout.get_layout()
        super().build_layout()

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe(
            layout.input_name,
            restrict_length(self.controller.name_max_len),
            base.with_element(
                make_text_update_handler(lambda x: x.title())
            )
        )

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(600, 300)
        ) | kwargs)

    def build_item(self, context: base.Context) -> T:
        item, values = self.item, context.values
        item.name = utils.strip(values[layout.input_name])
        item.is_producible = values[layout.checkbox_is_producible]
        return item


class EditResourceTypeView(EditItemView[ResourceType], AddResourceTypeView):
    title = utils.get_title("Изменение данных о типе ресурса")
    controller = inject.attr(ResourceTypesController)

    def dynamic_build(self):
        super().dynamic_build()
        self.window[layout.input_name].update(self.item.name)
        self.window[layout.checkbox_is_producible].update(self.item.is_producible)
