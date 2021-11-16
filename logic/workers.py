import inject

from dao.roles import RolesDAO
from dao.workers import WorkersDAO
from model import Worker


class WorkersController:
    source = inject.attr(WorkersDAO)
    roles_source = inject.attr(RolesDAO)

    name_max_len = 60
    name_min_len = 2

    def get_all(self):
        return self.source.get_all()

    def get_chief_candidates(self, worker: Worker):
        return self.source.get_chief_candidates(worker)\
                   .map(lambda data: [
                        (_id, f"{name}, {role}")
                        for _id, name, role in data])

    def get_count(self):
        return self.source.get_count()

    def get_roles(self):
        return self.roles_source.get_roles()

    def validate(self, worker: Worker):
        if not worker.name or len(worker.name) < self.name_min_len:
            return f"Длина ФИО не должна быть меньше {self.name_min_len}"

        if not worker.role_id:
            return "Не указана должность"

    def get_worker(self, _id: int):
        return self.source.get_item(_id)

    def add_worker(self, worker: Worker):
        error = self.validate(worker)
        if error:
            return error
        if not self.source.add_item(worker):
            return "Неизвестная ошибка"

    def update_worker(self, worker: Worker):
        error = self.validate(worker)
        if error:
            return error
        if not self.source.update_item(worker):
            return "Не удалось обновить данные"

    def delete_workers(self, *ids: int):
        if not self.source.delete_items(*ids):
            return "Удаление не удалось"
