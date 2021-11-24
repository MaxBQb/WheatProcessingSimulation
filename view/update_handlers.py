from typing import Union, Callable

import PySimpleGUI as sg

from logic.table import Table
from view import utils
from view.base import Context, with_element
from view.utils import max_len


def make_text_update_handler(text_format: Union[str, Callable[[str], str]] = "{}"):
    if isinstance(text_format, str):
        text_format = lambda x, tf=text_format: tf.format(x)

    def update_label(label: Union[sg.Text, sg.Input], context: Context):
        value = text_format(context.value)
        if value != context.value:
            if isinstance(label, sg.Input):
                label.update(value=value, move_cursor_to=None)
            else:
                label.update(value=value)
    return update_label


def update_listbox(element: sg.Listbox, values: list, selected: list[int] = None):
    if selected is None:
        selected = []
    disabled = element.Disabled
    element.update(disabled=False)
    element.update(values=values, set_to_index=selected)
    element.update(disabled=disabled)
    element.set_size((max(max_len(values), 24)+1, element.Size[1]))


def update_listbox_advanced(element: sg.Listbox, old: Table, new: Table) -> Table :
    selected = utils.get_new_selection(old, new, element.get_indexes())
    update_listbox(element, list(new.column(1)), selected)
    return new


def restrict_length(limit: int):
    return with_element(make_text_update_handler(
        lambda x: x[:limit]
    ))
