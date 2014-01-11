class Plugin:
    def __init__(self, channels):
        self.channels = channels

    def __call__(self, bot):
        bot.on_ready(self.on_ready)

    def on_ready(self, event):
        for channel in self.channels:
            event.bot.join(channel)
