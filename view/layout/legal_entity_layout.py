from .common import *

inputs = utils.Holder()

# ID's
input_name = inputs(auto_id())
input_address = inputs(auto_id())
input_phone = inputs(auto_id())


def get_layout():
    return [
        [utils.center(label("Заполните все поля"))],
        [label("Название"), inputElem(input_name)],
        [label("Адрес"), inputElem(input_address)],
        [label("Контактный номер"), inputElem(input_phone)],
    ]


def on_finalized(window: sg.Window):
    configure_inputs(window, *inputs.items)
