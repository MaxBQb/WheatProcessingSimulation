from .common import *


# ID's
from .styles import BUTTON_SUCCESS, BUTTON_ATTENTION

button_yes = auto_id()
button_no = auto_id()


def get_layout(message: str):
    return [
        [utils.center(sg.Text(message))],
        [utils.center(
            button("Да", button_yes, **BUTTON_SUCCESS),
            button("Нет", button_no, **BUTTON_ATTENTION),
        )],
    ]
