from dataclasses import dataclass
from yaml import load as load_yaml, Loader

from typing import List


@dataclass
class DBConfig:
    uri: str
    name: str


@dataclass
class Config:
    bot_token: str
    eth_api_key: str
    db: DBConfig
    admins: List[int]


CONFIG_FILENAME: str = "config.yml"


with open(CONFIG_FILENAME, "r", encoding="utf-8") as file:
    data: dict = load_yaml(
        stream = file,
        Loader = Loader
    )


config: Config = Config(
    db = DBConfig(
        **data.pop("db")
    ),
    **data
)


__all__ = (
    "config",
)
