import inject

from dao.standards import StandardsDAO, StandardsFilterOptions
from logic.items import ItemsController
from model import Standard


class StandardsController(ItemsController[Standard]):
    source = inject.attr(StandardsDAO)
    filter_type = StandardsFilterOptions

    name_max_len = 40
    name_min_len = 2
    description_max_len = 2000
    description_min_len = 2

    def validate(self, item: Standard):
        if not item.name or len(item.name) < self.name_min_len:
            return f"Длина названия не должна быть меньше {self.name_min_len}"

        if not item.description or len(item.description) < self.description_min_len:
            return f"Длина описания не должна быть меньше {self.description_min_len}"
