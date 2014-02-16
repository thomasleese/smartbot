import lxml.html
import requests


class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"(developer('s|s)? |programmer('s|s)? )?excuse( me)?", self.on_respond)
        bot.on_help("excuses", self.on_help)

    def on_respond(self, bot, msg, reply):
        page = requests.get("http://developerexcuses.com/")
        tree = lxml.html.fromstring(page.text)
        excuse = tree.cssselect(".wrapper a")[0].text_content()
        if excuse:
            reply(excuse)
        else:
            reply("You have no excuse!")

    def on_help(self, bot, msg, reply):
        reply("Syntax: [developer[']s|programmer[']s] excuse [me]")
