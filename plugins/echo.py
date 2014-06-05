import smartbot
from smartbot.formatting import *

class Plugin(smartbot.Plugin):
    """Reflect on what you say by getting SmartBot to echo it back at you."""
    names = ["echo", "print", "puts"]

    def on_command(self, msg, stdin, stdout, reply):
        print(*msg["args"][1:], file=stdout)

    def on_help(self):
        return "{}|{}|{} {}".format(
            self.bot.format("echo", Style.bold),
            self.bot.format("print", Style.bold),
            self.bot.format("puts", Style.bold),
            self.bot.format("something", Style.underline)
        )
