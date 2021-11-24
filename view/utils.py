import uuid
from typing import Hashable

import PySimpleGUI as sg

from logic.table import Table
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


SCROLLABLE_WINDOW = 'SCROLLABLE_WINDOW'


def make_scrollable(layout):
    return [[sg.Column(layout,
                       scrollable=True,
                       vertical_scroll_only=True,
                       key=SCROLLABLE_WINDOW,
                       expand_x=True)]]


def layout_from_fields(fields, base_key="-INPUT-", content_kwargs={}):
    description = dict(fields)
    size = (max_len(description.keys()) + 1, 1)
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
    try:
        return len(max(iterable, key=len))
    except ValueError:
        return 0


def first(array, default=None):
    return next(iter(array), default)


def strip(text: str = None):
    return (text or "").strip() or None


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


def get_new_selection(old: Table, new: Table, selected_rows: list[int], primary_column=0):
    return [
        list(new.column(primary_column)).index(
            old.cell(primary_column, selected_row)
        )
        for selected_row in selected_rows
        if old.cell(primary_column, selected_row, None) in new.column(primary_column)
    ]


def get_selected(table: Table, selected: list[int], primary=0):
    return (table.cell(primary, row) for row in selected)
