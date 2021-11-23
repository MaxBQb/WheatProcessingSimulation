from .common import *


# ID's
input_name = auto_id()
checkbox_is_producible = auto_id()


def get_layout():
    return [
        [utils.center(label("Заполните все поля"))],
        [label("Название типа"), input_elem(input_name)],
        [check_box("На продажу", checkbox_is_producible)],
    ]

