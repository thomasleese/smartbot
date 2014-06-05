from .exceptions import *

class Plugin:
    def __call__(self, bot):
        self.bot = bot

    def on_ready(self):
        pass

    def on_join(self, msg):
        pass

    def on_message(self, msg, reply):
        pass

    def on_respond(self, msg, reply):
        pass

    def on_command(self, msg, stdin, stdout, reply):
        raise NotImplementedError()
