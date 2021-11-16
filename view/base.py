from dataclasses import dataclass
from typing import Callable, Any, TypeVar
import PySimpleGUI as sg
from view.layout import EMPTY_LAYOUT
from typing import Hashable
from view.utils import get_title, center
from view.layout import submit_button
from view.livedata import LiveData
from event_system import MutableChannel, Channel

T = TypeVar("T")


@dataclass
class Context:
    window: sg.Window
    event: Hashable
    values: dict = None

    @property
    def value(self):
        return self.values[self.event]

    @value.setter
    def value(self, new_value):
        self.values[self.event] = new_value

    @property
    def element(self):
        return self.window[self.event]


def with_element(func):
    def wrapper(context: Context):
        return func(context.element, context)
    return wrapper


class BaseNonBlockingWindow:
    title = get_title("base non-blocking window")

    def __init__(self):
        self.window: sg.Window = None
        self.layout: list[list] = EMPTY_LAYOUT
        self.dependent_windows: set[BaseNonBlockingWindow] = set()

    def _add_dependency(self, dependent_window: 'BaseNonBlockingWindow'):
        self.dependent_windows.add(dependent_window)

    def _open_dependent_window(self, dependent_window: 'BaseNonBlockingWindow'):
        self._add_dependency(dependent_window)
        return dependent_window.run()

    def _close_dependent(self):
        for dependent in self.dependent_windows:
            dependent.send_close_event()

    def run(self):
        """
        Should be used to open window
        """
        self.build_layout()
        self.init_window()
        self.dynamic_build()

    def build_layout(self):
        pass

    def close(self):
        self._close_dependent()
        self.window.close()

    def send_close_event(self):
        if not self.window.was_closed():
            self.close()

    def init_window(self, **kwargs):
        self.window = sg.Window(
            self.title,
            self.layout,
            **(dict(
                finalize=True,
                alpha_channel=0,
                element_padding=(12, 12),
                size=(800, 600)
            ) | kwargs),
        )

    def dynamic_build(self):
        self.setup_window()
        self.window.alpha_channel = 1

    def setup_window(self):
        pass


class BaseInteractiveWindow(BaseNonBlockingWindow):
    HANDLER = Callable[[str, sg.Window, Any], None]

    title = get_title("base window")

    def __init__(self):
        super().__init__()
        self._channel: MutableChannel[Context] = MutableChannel()
        self.is_running = False

    @property
    def channel(self) -> Channel[Context]:
        return self._channel

    def run(self) -> Any:
        """
        Should be used to open window
        """
        self.build_layout()
        self.set_handlers()
        self.init_window()
        self.dynamic_build()
        self.dispatch_events()

    def close(self):
        self.is_running = False
        self._close_dependent()

    def send_close_event(self):
        if not self.window.was_closed():
            self.window.write_event_value(sg.WIN_CLOSED, None)

    def show_error(self, message: str = None):
        if not message:
            return
        self._open_dependent_window(ErrorView(message))
        return True

    def set_handlers(self):
        self.channel.subscribe(
            sg.WIN_CLOSED,
            lambda _: self.close(),
        )

    def run_event_loop(self):
        self.is_running = True
        while self.is_running:
            yield self.window.read()
        self.window.close()

    def dispatch_events(self):
        for event, values in self.run_event_loop():
            context = Context(self.window, event, values)
            self._channel.publish(event, context)

    def switchable_observe(self, _id: Hashable,
                           initial_livedata: LiveData,
                           func):
        def observe(livedata):
            return self.observe(_id, livedata, func)

        stop_holder = [observe(initial_livedata)]

        def switch(livedata: LiveData):
            stop_holder.pop()()
            stop_holder.append(observe(livedata))

        return switch

    def observe(self, _id: Hashable,
                livedata: LiveData,
                func):
        def on_update(context: Context):
            element = self.window[_id]
            func(element, context)

        return livedata.observe(
            self.window,
            self.channel,
            on_update,
            _id
        )


class ErrorView(BaseNonBlockingWindow):
    title = "Ошибка!"

    def __init__(self, message: str):
        super().__init__()
        self._message = message

    def build_layout(self):
        self.layout = [[
            sg.Text(self._message)
        ]] + [submit_button.get_layout(False)]

    def init_window(self, **kwargs):
        super().init_window(**dict(
            size=(None, None),
        ) | kwargs)
