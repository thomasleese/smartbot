import yaml

from . import Bot
from . import backends
from . import plugins
from . import stores


class Config:
    def __init__(self, filename="config.yaml"):
        with open(filename) as fd:
            self.config = yaml.load(fd.read())

    def _read_backend(self, config):
        name = config["name"]
        del config["name"]

        return getattr(backends, name).Backend(**config)

    def _read_storage(self, config):
        name = config["name"]
        del config["name"]

        return getattr(stores, name).Storage(**config)

    def _read_plugin(self, config):
        name = config["name"]
        del config["name"]

        return getattr(plugins, name).Plugin(**config)

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
