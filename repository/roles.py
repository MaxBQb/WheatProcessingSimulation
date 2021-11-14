from . import *
from dao.roles import RolesDAO


class RolesRepository:
    _dao = inject.attr(RolesDAO)

    @live_query(tables.role)
    def get_roles(self):
        return self._dao.get_roles()
