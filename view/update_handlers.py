import PySimpleGUI as sg
from view.base import Context


def make_text_update_handler(text_format: str = "{}"):
    def update_label(label: sg.Text, context: Context):
        label.update(value=text_format.format(context.value))
    return update_label
