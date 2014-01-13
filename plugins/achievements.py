import urllib.parse

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"achievement (?:got|get|unlock(?:ed)?) (.+)$", self.on_respond)
        bot.on_help("achievements", self.on_help)

    def on_respond(self, bot, msg, reply):
        url = "http://achievement-unlocked.heroku.com/xbox/{0}".format(urllib.parse.quote(msg["match"].group(1)))
        reply(url)

    def on_help(self, bot, reply):
        reply("Syntax: define <topic>")
