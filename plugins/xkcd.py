from smartbot import utils

class Plugin:
    def __call__(self, bot):
        bot.on_hear(r"xkcd\s+(\d+)", self.on_hear)
        bot.on_help("xkcd", self.on_help)

    def on_hear(self, bot, msg, reply):
        for num in msg["match"]:
            url = "http://xkcd.com/" + num
            reply("{0} -> {1}".format(url, utils.get_website_title(url)))

    def on_help(self, bot, msg, reply):
        reply("Syntax: xkcd <num>")
