class Plugin:
    def __init__(self, channel, password, target="NiceBot"):
        self.channel = channel
        self.password = password
        self.target = target

    def on_join(self, bot, msg):
        if self.channel == msg["channel"] and msg["is_me"]:
            bot.send(self.target, self.password)

    def on_help(self, bot):
        return "Authenticate with NiceBot."
