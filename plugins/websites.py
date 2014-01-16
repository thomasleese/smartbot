from smartbot import utils

class Plugin:
    def __call__(self, bot):
        bot.on_hear(r"(https?:\/\/[^\s]+)", self.on_hear)
        bot.on_help("websites", self.on_help)

    def on_hear(self, bot, msg, reply):
        for i, url in enumerate(msg["match"]):
            reply("[{0}]: {1}".format(i, utils.get_website_title(url)))

    def on_help(self, bot, msg, reply):
        reply("Echos the titles of websites for any HTTP(S) URL.")
