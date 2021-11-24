import inject

from dao.resources import ResourcesDAO, ResourceFilterOptions
from logic.flour_grades import FlourGradesController
from logic.grinding_grades import GrindingGradesController
from logic.items import ItemsController
from logic.resource_types import ResourceTypesController
from logic.table import Table
from model import Resource, ProductionLine


class ResourcesController(ItemsController[Resource]):
    source = inject.attr(ResourcesDAO)
    resource_types_source = inject.attr(ResourceTypesController)
    flour_grades_source = inject.attr(FlourGradesController)
    grinding_grades_source = inject.attr(GrindingGradesController)
    filter_type = ResourceFilterOptions

    description_max_len = 255
    description_min_len = 2

    def get_resource_types(self):
        return self.resource_types_source.get_all().map(Table)

    def get_flour_grades(self):
        return self.flour_grades_source.get_all().map(Table)

    def get_grinding_grades(self):
        return self.grinding_grades_source.get_all().map(Table)

    def validate(self, item: Resource):
        if not item.type_id:
            return "Не выбран тип ресурса"

        type_id = min(item.type_id, 5)

        return [
            self._validate_wheat,
            self._validate_brans,
            self._validate_flour,
            self._validate_flour_product,
            self._validate_ingredient,
        ][type_id-1](item)

    def _validate_wheat(self, item: Resource):
        item.description = None
        item.grinding_grade_id = None
        item.flour_grade_id = None

    def _validate_brans(self, item: Resource):
        item.description = None
        item.flour_grade_id = None

        if not item.grinding_grade_id:
            return "Должен быть указан сорт отрубей"

    def _validate_flour(self, item: Resource):
        item.description = None
        item.grinding_grade_id = None

        if not item.flour_grade_id:
            return "Должен быть указан сорт муки"

    def _validate_flour_product(self, item: Resource):
        item.flour_grade_id = None
        item.grinding_grade_id = None

        if not item.description or len(item.description) < self.description_min_len:
            return f"Длина описания не должна быть меньше {self.description_min_len}"

    def _validate_ingredient(self, item: Resource):
        item.flour_grade_id = None
        item.grinding_grade_id = None

        if not item.description or len(item.description) < self.description_min_len:
            return f"Длина описания не должна быть меньше {self.description_min_len}"

    def get_results_by_production_line(self, production_line: ProductionLine):
        return self.source.get_results_by_production_line(
            production_line.id
        )

    def get_resources_by_production_line(self, production_line: ProductionLine):
        return self.source.get_resources_by_production_line(
            production_line.id
        )