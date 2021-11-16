from . import *


def configure_inputs(window: sg.Window, *keys: str):
    utils.configure(
        *utils.elements_by_keys(window, *keys),
        **const.INPUT_EXTRA_DEFAULTS,
    )


def label(text: str):
    return sg.Text(f"{text}: ")


def inputElem(key: Hashable):
    return sg.Input(**const.INPUT_DEFAULTS, key=key, enable_events=True)


def button(text: str, key: Hashable, color=None, visible=True, **kwargs):
    return sg.pin(sg.Button(
        button_text=text,
        button_color=color,
        **const.BUTTON_DEFAULTS,
        visible=visible,
        key=key,
    ))


def choice_list(key: Hashable,
                length=50,
                select_mode=sg.SELECT_MODE_BROWSE,
                height=3):
    return sg.Listbox(
        [],
        **const.LIST_BOX_DEFAULTS,
        select_mode=select_mode,
        size=(length, height),
        enable_events=True,
        key=key,
    )
