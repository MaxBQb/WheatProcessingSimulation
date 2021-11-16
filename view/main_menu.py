
import PySimpleGUI as sg
import view.base as base
from view.layout import main_menu_layout as layout
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

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(640, 400)
        ) | kwargs)

    @base.transition
    def open_workers_view(self, _):
        return WorkersView()
