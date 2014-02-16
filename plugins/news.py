import requests
import urllib.parse


class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"news(?: about (.*))?$", self.on_respond)
        bot.on_help("news", self.on_help)

    def on_respond(self, bot, msg, reply):
        topic = msg["match"][0]
        if topic:
            url = "https://ajax.googleapis.com/ajax/services/search/news?v=1.0&rsz=5&q={0}".format(
                urllib.parse.quote(topic)
            )
        else:
            url = "https://ajax.googleapis.com/ajax/services/search/news?v=1.0&rsz=5&topic=h"

        headers = {"User-Agent": "SmartBot"}

        res = requests.get(url, headers=headers).json()
        stories = res["responseData"]["results"][:3]
        if stories:
            for i, story in enumerate(stories):
                title = story["titleNoFormatting"].replace("&#39;", "'").replace("`", "'").replace("&quot;", "\"")
                link = story["unescapedUrl"]
                reply("[{0}]: {1} - {2}".format(i, title, link))
        else:
            reply("No news stories.")

    def on_help(self, bot, msg, reply):
        reply("Syntax: news [about <topic>]")
