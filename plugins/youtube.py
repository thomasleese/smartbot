import re
import requests
import urllib

from smartbot import utils
from smartbot.formatting import *


class Plugin:
    def __init__(self, key):
        self.key = key

    def on_message(self, bot, msg, reply):
        match = re.findall(r"https?://(?:www\.)?youtube\.com/watch\?v=([^\s]+)", msg["message"], re.IGNORECASE)
        for i, id in enumerate(match):
            url = "https://www.googleapis.com/youtube/v3/videos?key={}&part=contentDetails%2Csnippet%2Cstatistics&id={}".format(
                urllib.parse.quote(self.key),
                urllib.parse.quote(id)
            )
            headers = {"User-Agent": "SmartBot"}
            payload = {
                "key": self.key,
                "id": id,
                "part": ",".join(["contentDetails", "snippet", "statistics"]),
            }

            res = requests.get(url, headers=headers).json()
            if res["items"]:
                video = res["items"][0]
                thumbnail = video["snippet"]["thumbnails"]["default"]["url"]
                duration = video["contentDetails"]["duration"]
                views = video["statistics"]["viewCount"]
                likes = video["statistics"]["likeCount"]
                dislikes = video["statistics"]["dislikeCount"]
                reply("{}: {} | {} {} {} | {}".format(bot.format("[{}]".format(i), Style.bold),
                                                      duration,
                                                      views,
                                                      bot.format(likes, Colour.fg_green),
                                                      bot.format(dislikes, Colour.fg_red),
                                                      bot.format(thumbnail, Colour.fg_grey)))

    def on_help(self):
        return "Sends information about YouTube URLs posted."
