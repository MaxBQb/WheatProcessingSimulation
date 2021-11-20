from .common import *


# ID's
checkbox_show_chiefs = auto_id()
checkbox_show_available = auto_id()


def get_layout():
    return [
        [[check_box('Показать только руководителей', checkbox_show_chiefs)]],
        [[check_box('Показать только незанятых', checkbox_show_available)]],
    ]

