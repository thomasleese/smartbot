import importlib

import yaml

from .bot import Bot


class Config:
    def __init__(self, filename="config.yaml"):
        with open(filename) as fd:
            self.config = yaml.load(fd.read())

    def _read_backend(self, config):
        name = config["name"]
        del config["name"]

        backend = importlib.import_module('smartbot.backends.{}'.format(name))
        return backend.Backend(**config)

    def _read_storage(self, config):
        name = config["name"]
        del config["name"]

        storage = importlib.import_module('smartbot.stores.{}'.format(name))
        return storage.Storage(**config)

    def _read_plugin(self, config):
        name = config["name"]
        del config["name"]

        plugin = importlib.import_module('smartbot.plugins.{}'.format(name))
        return plugin.Plugin(**config)

    def _read_plugins(self, config):
        return map(self._read_plugin, config)

    @property
    def bot(self):
        if not hasattr(self, "_bot"):
            self._bot = Bot(**self.config["bot"])
            self._bot.set_storage(self._read_storage(self.config["storage"]))
            self._bot.set_backend(self._read_backend(self.config["backend"]))
            self._bot.set_plugins(self._read_plugins(self.config["plugins"]))
        return self._bot
