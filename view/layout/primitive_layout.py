from .common import *


# ID's
input_name = auto_id()


def get_layout(name: str):
    return [
        [utils.center(label("Заполните поле ниже"))],
        [label(name.capitalize()), input_elem(input_name)],
    ]


def on_finalized(window: sg.Window):
    configure_inputs(window, input_name)
