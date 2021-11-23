import inject

from dao.resource_types import ResourceTypesDAO, ResourceTypeFilterOptions
from logic.items import ItemsController
from model import ResourceType


class ResourceTypesController(ItemsController[ResourceType]):
    source = inject.attr(ResourceTypesDAO)
    filter_type = ResourceTypeFilterOptions

    name_max_len = 40
    name_min_len = 2

    def validate(self, item: ResourceType):
        if not item.name or len(item.name) < self.name_min_len:
            return f"Длина названия не должна быть меньше {self.name_min_len}"
