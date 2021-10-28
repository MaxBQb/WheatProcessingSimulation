from contextlib import suppress
from dataclasses import dataclass

import jsons
import yaml

from mysql_config import MySQLConfig


@dataclass
class Config:
    mysql: MySQLConfig = MySQLConfig()


def make_config(filename: str) -> Config:
    config = None
    with suppress(FileNotFoundError, jsons.DecodeError):
        config = load_config(filename)
    if config is None:
        config = Config()
        save_config(config, filename)
    return config


def load_config(filename: str):
    with open(filename, "r", encoding="utf-8-sig") as f:
        content = yaml.load(f, yaml.SafeLoader)
        if content:
            return jsons.load(content, Config)


def save_config(config: Config, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(jsons.dump(config), f)
