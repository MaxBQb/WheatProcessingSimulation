from .common import *


# ID's
choice_list_type = auto_id()
checkbox_is_powered = auto_id()


def get_layout():
    return [
        [utils.center(label("Заполните все поля"))],
        [label("Вид станка")],
        [utils.center(choice_list(choice_list_type))],
        [check_box("Включен", checkbox_is_powered)],
    ]

