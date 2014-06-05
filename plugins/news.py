import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    names = ["news"]

    def on_command(self, msg, stdin, stdout, reply):
        topic = " ".join(msg["args"][1:])
        if not topic:
            topic = stdin.read().strip()

        url = "https://ajax.googleapis.com/ajax/services/search/news"
        payload = {
            "v": "1.0",
            "rsz": "5",
        }
        if topic:
            payload["q"] = topic
        else:
            payload["topic"] = "h"

        session = utils.web.requests_session()
        res = session.get(url, params=payload).json()
        stories = res["responseData"]["results"][:3]
        if stories:
            for i, story in enumerate(stories):
                title = story["titleNoFormatting"].replace("&#39;", "'").replace("`", "'").replace("&quot;", "\"")
                link = story["unescapedUrl"]
                print("[{0}]: {1} - {2}".format(i, title, link), file=stdout)
        else:
            raise StopCommand("No news stories.")

    def on_help(self):
        return "{} [{}]".format(
            self.bot.format("news", Style.bold),
            self.bot.format("topic", Style.underline),
        )
