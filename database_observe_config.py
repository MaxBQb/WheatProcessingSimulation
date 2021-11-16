from dataclasses import dataclass


@dataclass
class DatabaseObserverConfig:
    refresh_interval: float = 1
    check_interval: int = 10
