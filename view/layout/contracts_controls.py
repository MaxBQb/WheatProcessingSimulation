from .common import *
from ..radio_button import InteractiveRadioButton


radiobutton_show_finished = InteractiveRadioButton.optional_checkbox(
    "Только завершённые",
    "Только находящиеся в процессе",
    "Любые",
)

radiobutton_show_violated = InteractiveRadioButton.optional_checkbox(
    "Только нарушенные",
    "Только выполненные в срок",
    "Любые",
)


def get_layout():
    return [
        [*radiobutton_show_finished.radio_buttons],
        [*radiobutton_show_violated.radio_buttons],
    ]

