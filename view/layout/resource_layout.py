from .common import *

inputs = utils.Holder()

# ID's
input_description = inputs(auto_id())
choice_list_type = auto_id()
choice_list_flour_grade = auto_id()
choice_list_grinding_grade = auto_id()
slider_vitreousness = auto_id()
slider_contamination = auto_id()
section_wheat = auto_id()
section_bran = auto_id()
section_flour = auto_id()
section_description = auto_id()


def get_layout():
    return [
        [utils.center(label("Заполните все поля"))],
        [label("Тип ресурса")],
        [utils.center(choice_list(choice_list_type, height=5))],
        [sg.pin(sg.Column([
            [label("Стекловидность"),
             sg.Slider((0, 100),
                       orientation='horizontal',
                       key=slider_vitreousness)],
            [label("Загрязнённость"),
             sg.Slider((0, 100),
                       orientation='horizontal',
                       key=slider_contamination)],
        ], key=section_wheat, visible=False))],
        [sg.pin(sg.Column([
            [label("Помол отрубей")],
            [utils.center(choice_list(choice_list_grinding_grade, height=4))],
        ], key=section_bran, visible=False))],
        [sg.pin(sg.Column([
            [label("Сорт муки")],
            [utils.center(choice_list(choice_list_flour_grade, height=5))],
        ], key=section_flour, visible=False), expand_x=True)],
        [sg.pin(sg.Column([
            [label("Описание")],
            [utils.center(multiline_input(input_description))],
        ], key=section_description, visible=False))],
    ]


def on_finalized(window: sg.Window):
    configure_inputs(window, *inputs.items)
