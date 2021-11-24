from .common import *

inputs = utils.Holder()

# ID's
input_price = inputs(auto_id())
choice_list_legal_entity = auto_id()
choice_list_resources = auto_id()
label_creation_time = auto_id()
label_deadline_time = auto_id()
checkbox_is_finished = auto_id()


def get_layout(creation_mode: bool):
    return [
        [utils.center(label(
            "Заполните все поля"
            if creation_mode
            else "Текущие данные"
        ))],
        [label("Договор заключается с")],
        [utils.center(choice_list(choice_list_legal_entity))],
        [label("Ресурсы")],
        [utils.center(choice_list(
            choice_list_resources,
            select_mode=sg.SELECT_MODE_EXTENDED,
            disabled=not creation_mode,
            height=6))],
        [label("Сумма выплаты"), input_elem(input_price)],
        [sg.Text("Дата подписания:", key=label_creation_time)],
        [sg.Text("Крайняя дата завершения:", key=label_deadline_time,
                 visible=not creation_mode),
         check_box("Завершён", checkbox_is_finished, False)
        ],
    ]


def postprocess(layout):
    return utils.make_scrollable(layout)


def on_finalized(window: sg.Window):
    configure_inputs(window, *inputs.items)
    scrollable: sg.Column = window[utils.SCROLLABLE_WINDOW]
    scrollable.Widget.vscrollbar.pack_forget()
