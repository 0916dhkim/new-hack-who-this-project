# commands package
from .hello import hello
import logging


def add_commands():
    logging.info("Commands are added.")


__all__ = ["hello"]
