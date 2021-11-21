import uuid
from typing import Hashable

import PySimpleGUI as sg

from view.constants import APP_NAME, INPUT_DEFAULTS


def init_theme():
    sg.theme("DarkGray13")
    sg.set_options(
        icon="img/icon.ico",
    )


def get_title(title: str):
    return f"{APP_NAME}: {title.capitalize()}"


def hide(window, key: str):
    window[key].update(visible=False)


def set_underline(label: sg.Text, underline=True):
    label.update(font=(
        (*label.Font, 'underline')
        if underline
        else label.Font[:2]
    ))


def auto_id() -> Hashable:
    return uuid.uuid4().hex


def join_id(id_: str, *id_parts: str):
    return id_ + '-'.join(id_parts) + '-'


def center(*elements, **kwargs):
    return sg.Column([list(elements)],
                     pad=(0, 0),
                     justification='center', **kwargs)


def layout_from_fields(fields, base_key="-INPUT-", content_kwargs={}):
    description = dict(fields)
    size = (max_len(description.keys())+1, 1)
    font = INPUT_DEFAULTS['font']
    inputs = [
        join_id(base_key, name)
        for name in description
    ]
    layout = [[
            sg.Text(
                label.capitalize().replace('_', ' ') + ':',
                auto_size_text=False,
                font=font,
                size=size,
            ),
            sg.InputText(
                content,
                readonly=True,
                key=input_key,
                **INPUT_DEFAULTS,
                **content_kwargs
            )
        ]
        for (label, content), input_key
        in zip(description.items(), inputs)
    ]
    return layout, inputs


def max_len(iterable):
    return len(max(iterable, key=len))


def first(array, default=None):
    return next(iter(array), default)


def configure(*elements, **kwargs):
    for element in elements:
        element.Widget.config(
            **kwargs
        )


def elements_by_keys(window: sg.Window, *keys: Hashable):
    return (window[key] for key in keys)


class Holder:
    def __init__(self):
        self.items = []

    def __call__(self, value):
        self.items.append(value)
        return value
