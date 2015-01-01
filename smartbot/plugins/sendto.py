import smartbot.plugin
from smartbot.exceptions import StopCommandWithHelp
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Forward a message to a user."""
    names = ["sendto"]

    def on_command(self, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            user = msg["args"][1]
            message = " ".join(msg["args"][2:])
            if not message:
                message = stdin.read().strip()

            print("{0}: {1}".format(user, message), file=stdout)
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{} {} [{}]".format(
            super().on_help(),
            self.bot.format("user", Style.underline),
            self.bot.format("message", Style.underline)
        )
