from dataclasses import dataclass


@dataclass
class DatabaseObserverConfig:
    refresh_interval: int = 1
