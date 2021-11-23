import inject

from dao.roles import RolesDAO, RolesFilterOptions
from logic.primitives import PrimitiveController
from model import Role


class RolesController(PrimitiveController[Role]):
    source = inject.attr(RolesDAO)
    filter_type = RolesFilterOptions
    HEADER = "название должности"
