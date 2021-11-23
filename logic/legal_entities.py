from typing import Union

import inject
from dao.legal_entities import LegalEntitiesDAO, LegalEntitiesFilterOptions
from logic.items import ItemsController
from model import LegalEntity


class LegalEntitiesController(ItemsController[LegalEntity]):
    source = inject.attr(LegalEntitiesDAO)
    filter_type = LegalEntitiesFilterOptions

    name_max_len = 60
    name_min_len = 2
    address_max_len = 255
    phone_max_len = 15
    phone_min_len = 5

    def validate(self, item: LegalEntity):
        if not item.name or len(item.name) < self.name_min_len:
            return f"Длина названия не должна быть меньше {self.name_min_len}"

        if item.contact_phone and len(item.contact_phone) < self.phone_min_len:
            return f"Длина номера телефона не должна быть меньше {self.phone_min_len}"

    def format_phone(self, phone: Union[int, str]):
        return f"+{phone}"
