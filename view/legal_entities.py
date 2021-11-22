import PySimpleGUI as sg
import inject

import view.utils
from logic.table import Table
from logic.legal_entities import LegalEntitiesController
from model import LegalEntity
from view import utils as utils, base as base
from view.items import ItemsView, AddItemView, T, EditItemView
from view.layout import legal_entity_layout as layout
from view.update_handlers import restrict_length, make_text_update_handler, update_listbox


class LegalEntitiesView(ItemsView[LegalEntity]):
    title = view.utils.get_title("Поставщики и покупатели")
    controller = inject.attr(LegalEntitiesController)

    LABEL_CURRENT_COUNT = "Текущее количество юр.лиц: {}"

    TABLE_HEADERS = ["Название", "Адрес", "Контактный номер", "Рейтинг поставщика"]

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(1000, 400)
        ) | kwargs)

    def table_value_to_str(self, value, column: int, row: int):
        if column == 3 and value:
            return self.controller.format_phone(value)
        return super().table_value_to_str(value, column, row)

    @base.transition
    def open_add_item_view(self):
        return AddLegalEntityView()

    @base.transition
    def open_edit_item_view(self, _id: int):
        return EditLegalEntityView(_id)


class AddLegalEntityView(AddItemView[LegalEntity]):
    title = utils.get_title("Добавление юр.лица")
    controller = inject.attr(LegalEntitiesController)

    def __init__(self):
        super().__init__()
        self.item = LegalEntity()
        self.roles = Table()
        self.legal_entities = Table()
        self.chief_list_updater = None

    def build_layout(self):
        self.layout = layout.get_layout()
        super().build_layout()

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(600, 300)
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
            layout.input_phone,
            restrict_length(self.controller.phone_max_len),
            base.with_element(
                make_text_update_handler(
                    lambda x: ''.join(
                        list(filter(lambda y: y.isdigit(), x))
                    )
                )
            )
        )
        self.channel.subscribe(
            layout.input_address,
            restrict_length(self.controller.address_max_len),
        )

    def dynamic_build(self):
        super().dynamic_build()
        layout.on_finalized(self.window)

    def build_item(self, context: base.Context) -> T:
        item, values = self.item, context.values
        item.name = utils.strip(values[layout.input_name])
        item.address = utils.strip(values[layout.input_address])
        item.contact_phone = utils.strip(values[layout.input_phone])
        return item


class EditLegalEntityView(EditItemView[LegalEntity], AddLegalEntityView):
    title = utils.get_title("Изменение данных юр.лица")
    controller = inject.attr(LegalEntitiesController)

    def dynamic_build(self):
        super().dynamic_build()
        self.window[layout.input_name].update(self.item.name)
        self.window[layout.input_address].update(self.item.address)
        self.window[layout.input_phone].update(self.item.contact_phone)
