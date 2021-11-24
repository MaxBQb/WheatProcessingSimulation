from datetime import datetime, timedelta

import inject

from dao.machines import MachineFilterOptions
from dao.contracts import ContractsDAO, ContractFilterOptions
from dao.resources import ResourceFilterOptions
from dao.workers import WorkerFilterOptions
from logic.items import ItemsController
from logic.machines import MachinesController
from logic.resources import ResourcesController
from logic.roles import RolesController
from logic.legal_entities import LegalEntitiesController
from logic.table import Table
from logic.workers import WorkersController
from model import Contract


class ContractsController(ItemsController[Contract]):
    source = inject.attr(ContractsDAO)
    legal_entities_controller = inject.attr(LegalEntitiesController)
    resources_controller = inject.attr(ResourcesController)
    filter_type = ContractFilterOptions
    date_format = '%d.%m.%Y %H:%M:%S'

    def get_legal_entities(self):
        return self.legal_entities_controller.get_all().map(Table)

    def get_available_products(self):
        return self.resources_controller.get_all(ResourceFilterOptions(
            is_available=True,
            is_producible=True,
        )).map(lambda data: Table(
            [(_id, f"{name}, {description[:22]}" if description else name)
             for _id, name, description in data]
        ))

    def get_used_products(self, contract: Contract):
        return self.resources_controller.get_products_by_contract(
            contract
        ).map(lambda data: Table(
            [(_id, f"{name}, {description[:22]}" if description else name)
             for _id, name, description in data]
        ))
    
    def validate_update(self, item: Contract):
        if not item.legal_entity_id:
            return "Должна быть указана вторая сторона договора"

        if not item.price or item.price < 0:
            return "Должна быть указана цена (положительное число)"

        if item.is_finished and item.deadline_time < datetime.now():
            item.is_violated = True

    def validate(self, item: Contract):
        item.deadline_time = datetime.now() + timedelta(days=1)

        if not item.resources:
            return "Не указана продукция для продажи"

        return self.validate_update(item)
