import inject

from dao.machine_types import MachineTypesDAO
from logic.primitives import PrimitiveController
from model import MachineType


class MachineTypesController(PrimitiveController[MachineType]):
    source = inject.attr(MachineTypesDAO)
    HEADER = "название вида станков"
