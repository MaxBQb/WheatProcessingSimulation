import inject

from dao.machine_types import MachineTypesDAO, MachineTypesOptions
from logic.primitives import PrimitiveController
from model import MachineType


class MachineTypesController(PrimitiveController[MachineType]):
    source = inject.attr(MachineTypesDAO)
    filter_type = MachineTypesOptions
    HEADER = "название вида станков"
