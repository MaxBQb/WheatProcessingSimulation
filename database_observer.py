from threading import Thread
from time import sleep

import inject

from config import Config
from event_system import MutableChannel, Channel
from repository.changes import ChangesRepository


class DatabaseObserver:
    source = inject.attr(ChangesRepository)
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
            for event in self.source.get_changes(self.config.database_observer.check_interval):
                self._channel.publish(event, None)
            sleep(self.config.database_observer.refresh_interval)
