import inject

from dao.roles import RolesDAO
from logic.primitives import PrimitiveController
from model import Role


class RolesController(PrimitiveController[Role]):
    source = inject.attr(RolesDAO)
    HEADER = "название должности"
