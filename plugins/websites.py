import lxml.html
import requests

class Plugin:
    def __call__(self, bot):
        bot.on_hear(r"(https?:\/\/[^\s]+)", self.on_hear)
        bot.on_help("websites", self.on_help)

    def on_hear(self, bot, msg, reply):
        headers = { "User-Agent": "SmartBot" }
        for i, url in enumerate(msg["match"]):
            try:
                page = requests.get(url, headers=headers, timeout=3)
                if page.status_code == 200 and page.headers.get("Content-Type", "").startswith("text/html"):
                    tree = lxml.html.fromstring(page.content)
                    title = tree.cssselect("title")[0].text_content()
                    reply("[{0}]: {1}".format(i, title))
            except requests.exceptions.Timeout:
                reply("[{0}]: {1}".format(i, "Timeout!"))
            except IndexError: # no title element
                reply("[{0}]: {1}".format(i, "No title."))

    def on_help(self, bot, msg, reply):
        reply("Echos the titles of websites for any HTTP(S) URL.")
