import requests


class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"commit (message|msg)", self.on_respond)
        bot.on_help("commitmessage", self.on_help)

    def on_respond(self, bot, msg, reply):
        page = requests.get("http://whatthecommit.com/index.txt")
        if page.text:
            reply(page.text)
        else:
            reply("No Commit Message found.")

    def on_help(self, bot, msg, reply):
        reply("Syntax: commit message|msg")
