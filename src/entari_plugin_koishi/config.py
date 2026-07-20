from pathlib import Path

from arclet.entari import BasicConfModel, plugin_config


class Config(BasicConfModel):
    path: str | Path = "."


config = plugin_config(Config)
