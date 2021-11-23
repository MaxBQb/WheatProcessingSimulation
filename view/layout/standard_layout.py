from .common import *

inputs = utils.Holder()

# ID's
input_name = inputs(auto_id())
input_description = inputs(auto_id())


def get_layout():
    return [
        [utils.center(label("Заполните все поля"))],
        [label("Название"), input_elem(input_name)],
        [label("Описание")],
        [multiline_input(input_description)],
    ]


def on_finalized(window: sg.Window):
    configure_inputs(window, *inputs.items)
