import lxml.html
import requests

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"today in computer history|tdih|chm", self.on_respond)
        bot.on_help("chm", self.on_help)

    def on_respond(self, bot, msg, reply):
        page = requests.get("http://www.computerhistory.org/tdih/")
        tree = lxml.html.fromstring(page.text)
        event = tree.cssselect(".tdihevent p")[0].text_content()
        if event:
            reply(event)
        else:
            reply("Nothing happened today - that's a bit boring.")

    def on_help(self, bot, msg, reply):
        reply("Syntax: today in computer history|tdih|chm")
