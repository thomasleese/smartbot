import lxml.html
import requests

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"def(ine)? programming", self.on_respond)
        bot.on_help("defprogramming", self.on_help)

    def on_respond(self, bot, msg, reply):
        page = requests.get("http://www.defprogramming.com/random")
        tree = lxml.html.fromstring(page.text)
        definition = tree.cssselect("#main cite p")[0].text_content()
        if definition:
            reply(definition)
        else:
            reply("No definition today.")

    def on_help(self, bot, msg, reply):
        reply("Syntax: def[ine] programming")
