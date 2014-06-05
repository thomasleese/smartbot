class Plugin:
    """
    A plugin which automatically joins channels/rooms when the bot connects to
    the server.

    You should provide a list of channels to join in the plugin configuration,
    under the name 'channels'.
    """
    def __init__(self, channels):
        self.channels = channels

    def on_ready(self, bot):
        """Join all the channels."""
        for channel in self.channels:
            self.bot.join(channel)

    def on_help(self):
        """Get help about the plugin."""
        return "Automatically joins channels when the bot connects."
