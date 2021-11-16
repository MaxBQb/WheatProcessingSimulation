from .common import *


# ID's
button_workers = auto_id()
button_roles = auto_id()
button_standards = auto_id()
button_resources = auto_id()
button_resource_types = auto_id()
button_flour_grades = auto_id()
button_grinding_grades = auto_id()
button_production_lines = auto_id()
button_machines = auto_id()
button_machine_types = auto_id()
button_legal_entities = auto_id()
button_contracts = auto_id()


def get_layout():
    return [
        [[utils.center(
            sg.Text("Главное меню", font=('Tahoma', 14, 'bold')),
        )]],
        [
            sg.Column([
                [button('Сотрудники', button_workers)],
                [button('Должности', button_roles)],
                [button('Станки', button_machines)],
                [button('Виды станков', button_machine_types)],
            ], element_justification='center'),
            sg.Column([
                [button('Производство', button_production_lines)],
                [button('Стандарты производства', button_standards)],
                [button('Юридические лица', button_legal_entities)],
                [button('Договора', button_contracts)],
            ], element_justification='center'),
            sg.Column([
                [button('Ресурсы', button_resources)],
                [button('Типы ресурсов', button_resource_types)],
                [button('Помол отрубей', button_grinding_grades)],
                [button('Сорта муки', button_flour_grades)],
            ], element_justification='center'),
        ]
    ]
