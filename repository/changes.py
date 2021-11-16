import inject

from dao.changes import ChangesDAO


class ChangesRepository:
    _dao = inject.attr(ChangesDAO)

    def __init__(self):
        self._current_state = {}

    def get_changes(self, update_interval: int):
        new_state = self._dao.get_all_changes(update_interval)
        new_state = dict(new_state)
        diff = {
            k for k, v in new_state.items()
            if self._current_state.get(k, "New Value") != v
        }
        self._current_state |= new_state
        return diff
