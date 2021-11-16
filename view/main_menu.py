import view.base as base
from view.flour_grades import FlourGradesView
from view.grinding_grades import GrindingGradesView
from view.layout import main_menu_layout as layout
from view.machine_types import MachineTypesView
from view.roles import RolesView
from view.workers import WorkersView


class MainMenuView(base.BaseInteractiveWindow):

    def build_layout(self):
        self.layout = layout.get_layout()

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe(
            layout.button_workers,
            self.open_workers_view
        )
        self.channel.subscribe(
            layout.button_roles,
            self.open_roles_view
        )
        self.channel.subscribe(
            layout.button_machine_types,
            self.open_machine_types_view
        )
        self.channel.subscribe(
            layout.button_flour_grades,
            self.open_flour_grades_view
        )
        self.channel.subscribe(
            layout.button_grinding_grades,
            self.open_grinding_grades_view
        )

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(640, 400)
        ) | kwargs)

    @base.transition
    def open_workers_view(self, _):
        return WorkersView()

    @base.transition
    def open_roles_view(self, _):
        return RolesView()

    @base.transition
    def open_machine_types_view(self, _):
        return MachineTypesView()

    @base.transition
    def open_flour_grades_view(self, _):
        return FlourGradesView()

    @base.transition
    def open_grinding_grades_view(self, _):
        return GrindingGradesView()
