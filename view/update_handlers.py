from typing import Union, Callable

import PySimpleGUI as sg
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


def update_listbox(element: sg.Listbox, values: list):
    element.update(values=values)
    element.set_size((max_len(values)+1, element.Size[1]))


def restrict_length(limit: int):
    return with_element(make_text_update_handler(
        lambda x: x[:limit]
    ))
