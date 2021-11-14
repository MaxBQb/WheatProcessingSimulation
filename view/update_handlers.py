import PySimpleGUI as sg
from view.base import Context
from view.utils import max_len


def make_text_update_handler(text_format: str = "{}"):
    def update_label(label: sg.Text, context: Context):
        label.update(value=text_format.format(context.value))
    return update_label


def update_listbox(element: sg.Listbox, values: list):
    element.update(values=values)
    element.set_size((max_len(values)+1, element.Size[1]))


def restrict_length(max_len: int):
    def on_input(context: Context):
        element: sg.Input = context.element
        if len(context.value) > max_len:
            element.update(value=context.value[:max_len])
    return on_input
