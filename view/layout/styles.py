from view.constants import BUTTON_DEFAULTS

DEFAULT_FONT = ('Tahoma', 10)

BUTTON_NORMAL = BUTTON_DEFAULTS | dict(
    font=DEFAULT_FONT,
)

BUTTON_SUCCESS = dict(
    button_color=('Black', 'DarkGreen'),
)

BUTTON_NEW = dict(
    button_color=('Black', 'Green'),
)

BUTTON_ATTENTION = dict(
    button_color='DarkRed',
)
