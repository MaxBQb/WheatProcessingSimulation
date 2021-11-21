from .common import *
from ..radio_button import InteractiveRadioButton


# ID's
checkbox_show_chiefs = auto_id()
checkbox_show_available = auto_id()

radiobutton_show_chiefs = InteractiveRadioButton.optional_checkbox(
    "Только руководители",
    "Только сотрудники без подчинённых",
    "Любые",
)


def get_layout():
    return [
        [*radiobutton_show_chiefs.radio_buttons],
        [[check_box('Показать только незанятых', checkbox_show_available)]],
    ]

