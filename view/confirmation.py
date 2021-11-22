import inject

import view.base as base
from logic.workers import WorkersController
from view.layout import confirm_dialog_layout as layout


class ConfirmDialogView(base.BaseInteractiveWindow):
    title = "Требуется подтверждение"
    controller = inject.attr(WorkersController)

    def __init__(self, message: str, default=False):
        super().__init__()
        self.message = message
        self.result = default

    def build_layout(self):
        self.layout = layout.get_layout(self.message)

    def run(self) -> bool:
        super().run()
        self.window_manager.await_window_closed(self.window)
        return self.result

    def setup_window(self):
        super().setup_window()
        self.window.set_min_size((400, 120))

    def set_handlers(self):
        super().set_handlers()
        self.channel.subscribe_foreach(
            (layout.button_yes, layout.button_no),
            self.on_button_pressed
        )

    def on_button_pressed(self, context: base.Context):
        self.result = context.event == layout.button_yes
        self.close()
