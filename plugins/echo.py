from smartbot.formatting import *

class Plugin:
    """Reflect on what you say by getting SmartBot to echo it back at you."""
    def on_command(self, bot, msg, stdin, stdout, reply):
        print(*msg["args"][1:], file=stdout)

    def on_help(self):
        return "{} {}".format(
            self.bot.format("echo", Style.bold),
            self.bot.format("something", Style.underline)
        )
