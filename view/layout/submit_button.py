from . import *


# ID's
button_submit = auto_id()


def get_layout(form=True):
    return [utils.center(sg.Button(
        key=button_submit,
        **(const.BUTTON_DEFAULTS | dict(
            button_text="OK",
            pad=(6, 6),
            bind_return_key=True,
            auto_size_button=False,
            button_type=sg.BUTTON_TYPE_READ_FORM
            if form else sg.BUTTON_TYPE_CLOSES_WIN_ONLY,
        ))
    ))]