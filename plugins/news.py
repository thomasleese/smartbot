import requests
import urllib.parse
import sys


class Plugin:
    def on_command(self, bot, msg):
        topic = " ".join(sys.argv[1:])
        if not topic:
            topic = sys.stdin.read().strip()

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
                print("[{0}]: {1} - {2}".format(i, title, link))
        else:
            print("No news stories.")

    def on_help(self):
        return "Syntax: news [<topic>]"
