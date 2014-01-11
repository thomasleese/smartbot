class Plugin:
    def __init__(self, channel, password, user="NiceBot"):
        self.channel = channel
        self.password = password
        self.user = user

    def __call__(self, bot):
        bot.on_join(self.on_join)

    def on_join(self, event):
        if event.channel == self.channel and event.is_me:
            event.bot.send(self.user, self.password)
