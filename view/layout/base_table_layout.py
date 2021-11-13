import PySimpleGUI

from . import *

# ID's
label_entries_count = auto_id()
table_entries = auto_id()


def get_layout(table_headers: list[str]):
    return [
        [utils.center(
            sg.Text("Текущее количество:"),
            sg.Text("0", key=label_entries_count),
        )],
        [
            [utils.center(sg.Table(
                values=[[""]*(len(table_headers)+1)],
                headings=['id']+table_headers,
                visible_column_map=[False]+[True]*len(table_headers),
                select_mode=PySimpleGUI.TABLE_SELECT_MODE_EXTENDED,
                justification='center',
                hide_vertical_scroll=True,
                expand_x=True,
                key=table_entries,
            ), expand_x=True)]
        ],
    ]
