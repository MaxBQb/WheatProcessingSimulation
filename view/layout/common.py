from . import *
from .styles import BUTTON_NORMAL, DEFAULT_FONT


def configure_inputs(window: sg.Window, *keys: str):
    utils.configure(
        *utils.elements_by_keys(window, *keys),
        **const.INPUT_EXTRA_DEFAULTS,
    )


def label(text: str):
    return sg.Text(f"{text}: ")


def slider(min_v: int, max_v: int, key: Hashable, tick=20):
    return sg.Slider(
        (min_v, max_v),
        orientation='horizontal',
        key=key,
        resolution=1,
        tick_interval=tick
    )


def input_elem(key: Hashable):
    return sg.Input(**const.INPUT_DEFAULTS, key=key, enable_events=True)


def multiline_input(key: Hashable):
    return sg.Multiline(**const.MULTILINE_DEFAULTS,
                        key=key,
                        size=(600, 8),
                        autoscroll=True,
                        enable_events=True)


def button(text: str, key: Hashable, **kwargs):
    return sg.pin(sg.Button(
        button_text=text,
        **(BUTTON_NORMAL | kwargs),
        key=key,
    ))


def choice_list(key: Hashable,
                length=50,
                select_mode=sg.SELECT_MODE_BROWSE,
                height=3, disabled=False):
    return sg.Listbox(
        [],
        **const.LIST_BOX_DEFAULTS,
        select_mode=select_mode,
        size=(length, height),
        enable_events=not disabled,
        disabled=disabled,
        key=key,
    )


def check_box(text: str, key: Hashable, visible=True):
    return sg.Checkbox(
        text,
        enable_events=True,
        visible=visible,
        font=(DEFAULT_FONT[0], DEFAULT_FONT[1]+2),
        key=key,
    )
