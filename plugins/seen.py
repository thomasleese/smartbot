import datetime

class Plugin:
    def __call__(self, bot):
        bot.on_hear(r".*", self.on_hear)
        bot.on_respond(r"(?:last )?seen (.*)$", self.on_respond)
        bot.on_help("steam", self.on_help)

    def on_hear(self, bot, msg, reply):
        bot.storage["seen." + msg["sender"]] = {
            "action": "spoke",
            "datetime": datetime.datetime.now()
        }

    def on_respond(self, bot, msg, reply):
        try:
            info = bot.storage["seen." + msg["match"][0]]
            reply("{0} {1} on {2}.".format(msg["match"][0], info["action"], info["datetime"].strftime("%a %d %b %H:%M %Z").strip()))
        except KeyError:
            reply("I don't know anything about {0}.".format(msg["match"][0]))

    def on_help(self, bot, msg, reply):
        reply("Syntax: [last] seen <user>")
