from .common import *
from .styles import BUTTON_SUCCESS, BUTTON_ATTENTION, BUTTON_NEW


inputs = utils.Holder()

# ID's
input_search = inputs(auto_id())
label_entries_count = auto_id()
table_entries = auto_id()
button_add = auto_id()
button_edit = auto_id()
button_delete = auto_id()


def get_layout(table_headers: list[str]):
    return [
        [utils.center(
            sg.Text("Текущее количество: 0", key=label_entries_count),
        )],
        [
            [utils.center(sg.Table(
                values=[[""]*(len(table_headers)+1)],
                headings=['id']+table_headers,
                visible_column_map=[False]+[True]*len(table_headers),
                select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                justification='center',
                hide_vertical_scroll=True,
                expand_x=True,
                enable_events=True,
                key=table_entries,
            ), expand_x=True)]
        ],
        [
            [utils.center(
                button('Добавить', button_add, **BUTTON_NEW),
                button('Изменить', button_edit, **BUTTON_SUCCESS),
                button('Удалить', button_delete, **BUTTON_ATTENTION),
            )]
        ],
        [label("Поиск"), input_elem(input_search)],
    ]


def on_finalized(window: sg.Window):
    configure_inputs(window, *inputs.items)
