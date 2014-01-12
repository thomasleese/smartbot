class Plugin:
    def __init__(self, channel, password, target="NiceBot"):
        self.channel = channel
        self.password = password
        self.target = target

    def __call__(self, bot):
        bot.on_join(self.on_join)

    def on_join(self, bot, msg):
        if self.channel == msg["channel"] and msg["is_me"]:
            bot.send(self.target, self.password)
