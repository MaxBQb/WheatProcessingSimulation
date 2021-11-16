from . import *
from .common import button


# ID's
button_submit = auto_id()


def get_layout(form=True):
    return [utils.center(button(
        "OK",
        button_submit,
        **dict(
            pad=(6, 6),
            bind_return_key=True,
            auto_size_button=False,
            button_type=sg.BUTTON_TYPE_READ_FORM
            if form else sg.BUTTON_TYPE_CLOSES_WIN_ONLY,
        )
    ))]
