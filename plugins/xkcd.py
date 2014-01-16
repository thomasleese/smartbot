import lxml.html
import requests

class Plugin:
    def __call__(self, bot):
        bot.on_hear(r"xkcd\s+(\d+)", self.on_hear)
        bot.on_help("xkcd", self.on_help)

    def on_hear(self, bot, msg, reply):
        headers = { "User-Agent": "SmartBot" }
        for num in msg["match"]:
            url = "http://xkcd.com/" + num
            try:
                page = requests.get(url, headers=headers, timeout=3)
                if page.status_code == 200 and page.headers.get("Content-Type", "").startswith("text/html"):
                    tree = lxml.html.fromstring(page.content)
                    title = tree.cssselect("title")[0].text_content()
                    reply("{0} -> {1}".format(url, title))
            except requests.exceptions.Timeout:
                reply("{0}".format(url))

    def on_help(self, bot, msg, reply):
        reply("Syntax: xkcd <num>")
