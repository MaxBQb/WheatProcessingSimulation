import view.base as base
from view.flour_grades import FlourGradesView
from view.grinding_grades import GrindingGradesView
from view.layout import main_menu_layout as layout
from view.machine_types import MachineTypesView
from view.roles import RolesView
from view.workers import WorkersView


class MainMenuView(base.BaseInteractiveWindow):
    def __init__(self):
        super().__init__()
        self._ways = (
            (layout.button_workers, self.open_workers_view),
            (layout.button_roles, self.open_roles_view),
            (layout.button_machine_types, self.open_machine_types_view),
            (layout.button_flour_grades, self.open_flour_grades_view),
            (layout.button_grinding_grades, self.open_grinding_grades_view),
        )

    def build_layout(self):
        self.layout = layout.get_layout()

    def set_handlers(self):
        super().set_handlers()
        for _id, transition in self._ways:
            self.channel.subscribe(
                _id,
                self.mark('Green', False),
                transition,
                self.mark('Dark Green', True),
            )

    def dynamic_build(self):
        super().dynamic_build()
        for _id, _ in self._ways:
            self.window[_id].update(button_color='#555')

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(640, 400)
        ) | kwargs)

    def mark(self, color: str, is_enabled: bool):
        def on_event(context: base.Context):
            for _id, _ in self._ways:
                self.window[_id].update(disabled=not is_enabled,
                                        button_color="#555" if is_enabled else "#444")
            context.element.update(button_color=color)
        return on_event

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
