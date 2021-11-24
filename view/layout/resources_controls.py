from .common import *
from ..radio_button import InteractiveRadioButton


# ID's
checkbox_show_available = auto_id()
checkbox_show_planned = auto_id()

radiobutton_show_producible = InteractiveRadioButton.optional_checkbox(
    "Только на продажу",
    "Только закупленные",
    "Любые",
)


def get_layout():
    return [
        [*radiobutton_show_producible.radio_buttons],
        [[check_box('Показать только доступные', checkbox_show_available)]],
        [[check_box('Показать только запланированные', checkbox_show_planned)]],
    ]

