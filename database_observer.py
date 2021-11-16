from threading import Thread
from time import sleep

import inject

from config import Config
from dao.changes import ChangesDAO
from event_system import MutableChannel, Channel


class DatabaseObserver:
    source = inject.attr(ChangesDAO)
    config = inject.attr(Config)

    class Event:
        contract = "contract"
        flour_grade = "flour_grade"
        grinding_grade = "grinding_grade"
        legal_entity = "legal_entity"
        machine = "machine"
        machine_to_production_line = "machine_to_production_line"
        machine_type = "machine_type"
        production_line = "production_line"
        resource = "resource"
        resource_type = "resource_type"
        role = "role"
        standard = "standard"
        worker = "worker"
        worker_to_production_line = "worker_to_production_line"

    def __init__(self):
        self._channel: MutableChannel[None] = MutableChannel()
        self._current_state = {}
        self._thread = Thread(
            name="DatabasePolling",
            target=self._poll_db,
            daemon=True
        )

    @property
    def channel(self) -> Channel[None]:
        return self._channel

    def run(self):
        self._thread.start()

    def _poll_db(self):
        while True:
            for event in self._get_changes():
                self._channel.publish(event, None)
            sleep(self.config.database_observer.refresh_interval)

    def _get_changes(self):
        new_state = self.source.get_all_changes(self.config.database_observer.check_interval)
        new_state = dict(new_state)
        diff = {
            k for k, v in new_state.items()
            if self._current_state.get(k, "New Value") != v
        }
        self._current_state |= new_state
        return diff
