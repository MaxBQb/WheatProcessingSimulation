from .common import *

inputs = utils.Holder()

# ID's
input_name = inputs(auto_id())
choice_list_standard = auto_id()
choice_list_resources = auto_id()
choice_list_workers = auto_id()
choice_list_machines = auto_id()
choice_list_results = auto_id()
label_start_time = auto_id()
label_finish_time = auto_id()
button_finish = auto_id()
button_reset_finish = auto_id()


def get_layout(creation_mode: bool):
    return [
        [utils.center(label(
            "Заполните все поля"
            if creation_mode
            else "Текущие данные"
        ))],
        [label("Стандарт")],
        [utils.center(choice_list(choice_list_standard))],
        [label("Необходимые ресурсы")],
        [utils.center(choice_list(
            choice_list_resources,
            select_mode=sg.SELECT_MODE_EXTENDED,
            disabled=not creation_mode,
            height=6))],
        [label("Результат на выходе")],
        [utils.center(choice_list(
            choice_list_results,
            select_mode=sg.SELECT_MODE_EXTENDED,
            disabled=not creation_mode,
            height=6))],
        [label("Привлечённые сотрудники")],
        [utils.center(choice_list(
            choice_list_workers,
            select_mode=sg.SELECT_MODE_EXTENDED,
            disabled=not creation_mode,
            height=6))],
        [label("Использованные станки")],
        [utils.center(choice_list(
            choice_list_machines,
            select_mode=sg.SELECT_MODE_EXTENDED,
            disabled=not creation_mode,
            height=6))],
        [sg.Text("Дата начала:", key=label_start_time)],
        [sg.Text("Дата завершения:",
                 key=label_finish_time,
                 visible=not creation_mode),
            button("Завершить", button_finish,
                   visible=not creation_mode),
            button("❌", button_reset_finish,
                   visible=not creation_mode)
         ]
    ]


def postprocess(layout):
    return utils.make_scrollable(layout)


def on_finalized(window: sg.Window):
    scrollable: sg.Column = window[utils.SCROLLABLE_WINDOW]
    scrollable.Widget.vscrollbar.pack_forget()
