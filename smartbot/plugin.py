from .exceptions import *
from .formatting import Style

class Plugin:
    disable_plugins = []

    def __call__(self, bot):
        self.bot = bot

    def on_ready(self):
        pass

    def on_join(self, msg):
        pass

    def pre_on_message(self, handler, msg):
        pass

    def on_message(self, msg, reply):
        pass

    def pre_on_respond(self, handler, msg):
        pass

    def on_respond(self, msg, reply):
        pass

    def on_command(self, msg, stdin, stdout, reply):
        raise NotImplementedError()

    def on_help(self):
        _bold = lambda s: self.bot.format(s, Style.bold)
        return "|".join(map(_bold, self.names))
