from .common import *

inputs = utils.Holder()

# ID's
input_name = inputs(auto_id())
choice_list_role = auto_id()
choice_list_chief = auto_id()


def get_layout():
    return [
        [utils.center(label("Заполните все поля"))],
        [label("ФИО"), input_elem(input_name)],
        [label("Должность")],
        [utils.center(choice_list(choice_list_role))],
        [label("Руководитель")],
        [utils.center(choice_list(choice_list_chief, height=6))],
    ]


def on_finalized(window: sg.Window):
    configure_inputs(window, *inputs.items)
