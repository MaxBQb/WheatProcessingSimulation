from .common import *


# ID's
button_yes = auto_id()
button_no = auto_id()


def get_layout(message: str):
    return [
        [utils.center(sg.Text(message))],
        [utils.center(
            button("Да", button_yes, "DarkGreen"),
            button("Нет", button_no, "DarkRed"),
        )],
    ]
