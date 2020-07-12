# commands package
from .hello import hello
from .mood import mood
import logging


def add_commands():
    logging.info("Commands are added.")


__all__ = ["hello", "mood"]
