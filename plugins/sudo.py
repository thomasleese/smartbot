class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"sudo(?: )?(.*)$", self.on_respond)

    def on_respond(self, bot, msg, reply):
        if msg["match"][0]:
            s = msg["match"][0].lower().replace("me", "you")
            reply("Alright, I'll {0}.".format(s))
        else:
            reply("Alright, I'll do whatever it is you want.")
