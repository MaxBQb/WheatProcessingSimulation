import PySimpleGUI as sg

APP_NAME = "Переработка пшеницы"
BUTTON_DEFAULTS = dict(
    mouseover_colors="#333333",
    disabled_button_color="#21242c",
)

ICON_BUTTON_DEFAULTS = lambda: dict(
    button_color=(sg.theme_background_color(), sg.theme_background_color()),
    border_width=0,
)
INPUT_DEFAULTS = dict(
    disabled_readonly_background_color="#222",
    font=('Consolas', 12)
)
LIST_BOX_DEFAULTS = dict(
    background_color="#313131",
    no_scrollbar=True,
    font=INPUT_DEFAULTS['font'],
    highlight_background_color="#515151",
    highlight_text_color="#cecece",
)
INPUT_EXTRA_DEFAULTS = dict(
    insertwidth='4',
    insertbackground='silver',
    selectbackground='#175924',
    selectforeground='silver',
)
