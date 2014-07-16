from .bot import Bot
from .plugin import Plugin
from .backend import Backend
from .storage import Storage
from .config import Config
from . import utils
from . import formatting


def main():
    config = Config()
    config.bot.run()
