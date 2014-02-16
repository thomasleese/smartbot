import urllib.parse


class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"lmgtfy (.*)$", self.on_respond)
        bot.on_help("lmgtfy", self.on_help)

    def on_respond(self, bot, msg, reply):
        url = "http://lmgtfy.com/?q={0}".format(urllib.parse.quote(msg["match"][0]))
        reply(url)

    def on_help(self, bot, msg, reply):
        reply("Syntax: lmgtfy <query>")
