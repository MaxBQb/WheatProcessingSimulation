import view.base as base
from view import utils
from view.flour_grades import FlourGradesView
from view.grinding_grades import GrindingGradesView
from view.layout import main_menu_layout as layout
from view.legal_entities import LegalEntitiesView
from view.machine_types import MachineTypesView
from view.machines import MachinesView
from view.roles import RolesView
from view.workers import WorkersView


class MainMenuView(base.BaseInteractiveWindow):
    title = utils.get_title("Главное меню")

    def __init__(self):
        super().__init__()
        self._ways = (
            (layout.button_workers, WorkersView),
            (layout.button_roles, RolesView),
            (layout.button_machine_types, MachineTypesView),
            (layout.button_flour_grades, FlourGradesView),
            (layout.button_grinding_grades, GrindingGradesView),
            (layout.button_machines, MachinesView),
            (layout.button_legal_entities, LegalEntitiesView),
        )

    def build_layout(self):
        self.layout = layout.get_layout()

    def set_handlers(self):
        super().set_handlers()
        for _id, _class in self._ways:
            self.channel.subscribe(
                _id,
                self.mark('Green'),
                lambda _, cls=_class: self.go_to(cls),
                self.mark('Dark Green'),
            )

    @base.transition
    def go_to(self, window):
        return window()

    def dynamic_build(self):
        super().dynamic_build()
        for _id, _ in self._ways:
            self.window[_id].update(button_color='#555')

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(640, 400)
        ) | kwargs)

    def mark(self, color: str):
        def on_event(context: base.Context):
            for _id, _ in self._ways:
                self.window[_id].update(button_color="#555")
            context.element.update(button_color=color)
        return on_event
