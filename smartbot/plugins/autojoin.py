import smartbot.plugin
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """
    A plugin which automatically joins channels/rooms when the bot connects to
    the server.

    You should provide a list of channels to join in the plugin configuration,
    under the name 'channels'.
    """
    names = ["autojoin"]

    def __init__(self, channels):
        self.channels = channels

    def on_ready(self):
        """Join all the channels."""
        for channel in self.channels:
            self.bot.join(channel)

    def on_command(self, msg, stdin, stdout):
        print(" ".join(self.channels), file=stdout)

    def on_help(self):
        """Get help about the plugin."""
        return "{}".format(self.bot.format("autojoin", Style.bold))
