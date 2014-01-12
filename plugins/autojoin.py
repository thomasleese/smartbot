class Plugin:
    def __init__(self, channels):
        self.channels = channels

    def __call__(self, bot):
        bot.on_ready(self.on_ready)
        bot.on_help("autojoin", self.on_help)

    def on_ready(self, bot):
        for channel in self.channels:
            bot.join(channel)

    def on_help(self, bot, reply):
        reply("Automatically joins channels when the bot connects.")
