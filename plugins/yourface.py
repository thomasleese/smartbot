class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"your face is .+$", self.on_respond)
        bot.on_help("yourface", self.on_help)

    def on_respond(self, bot, msg, reply):
        reply("Oh yeah… well, your face is…")
        reply("!face " + msg["sender"])

    def on_help(self, bot, msg, reply):
        reply("That's right!")
