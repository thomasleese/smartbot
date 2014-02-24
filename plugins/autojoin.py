class Plugin:
    def __init__(self, channels):
        self.channels = channels

    def on_ready(self, bot):
        for channel in self.channels:
            bot.join(channel)

    def on_help(self):
        return "Automatically joins channels when the bot connects."
