import lxml.html
import requests

from smartbot import utils

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"humble( weekly)?( sale)?", self.on_respond)
        bot.on_help("humble", self.on_help)

    def on_respond(self, bot, msg, reply):
        page = requests.get("https://www.humblebundle.com/weekly")
        tree = lxml.html.fromstring(page.text)
        try:
            title = tree.cssselect("title")[0].text_content().strip()
            clock = tree.cssselect("#heading-time-remaining .mini-digit-holder")[0]
            c0 = clock.cssselect(".c0 .heading-num")[0].text_content()
            c1 = clock.cssselect(".c1 .heading-num")[0].text_content()
            c2 = clock.cssselect(".c2 .heading-num")[0].text_content()
            c3 = clock.cssselect(".c3 .heading-num")[0].text_content()
            c4 = clock.cssselect(".c4 .heading-num")[0].text_content()
            c5 = clock.cssselect(".c5 .heading-num")[0].text_content()
            c6 = clock.cssselect(".c6 .heading-num")[0].text_content()
            c7 = clock.cssselect(".c7 .heading-num")[0].text_content()
            reply("{0} - {1}{2}:{3}{4}:{5}{6}:{7}{8} left".format(title, c0, c1, c2, c3, c4, c5, c6, c7))
        except IndexError:
            reply("No weekly sale.")

    def on_help(self, bot, msg, reply):
        reply("Syntax: humble [weekly] [deal]")
