from .common import *
from ..radio_button import InteractiveRadioButton


# ID's
checkbox_show_available = auto_id()


radiobutton_show_powered = InteractiveRadioButton.optional_checkbox(
    "Только включённые",
    "Только отключенные",
    "Любые",
)


def get_layout():
    return [
        [radiobutton_show_powered.radio_buttons],
        [[check_box('Показать только незанятые', checkbox_show_available)]],
    ]

