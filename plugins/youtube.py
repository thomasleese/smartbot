import re
import urllib

import isodate
import requests

from smartbot import utils
from smartbot.formatting import *


REGEX = r"(?:https?://)?(?:www\.)?youtu\.?be(?:\.com)?/(?:watch\?v=)?([^\s]+)"


class Plugin:
    def __init__(self, key):
        self.key = key

    def _get_reply(self, bot, i, video):
        channelTitle = video["snippet"]["channelTitle"]
        duration = isodate.parse_duration(video["contentDetails"]["duration"])
        views = video["statistics"]["viewCount"]
        likes = video["statistics"]["likeCount"]
        dislikes = video["statistics"]["dislikeCount"]
        thumbnail = video["snippet"]["thumbnails"]["default"]["url"]

        format_string = "{}: {} | {} | {} {} {} | {}"
        return format_string.format(bot.format("[{}]".format(i), Style.bold),
                                    channelTitle,
                                    duration,
                                    views,
                                    bot.format(likes, Colour.fg_green),
                                    bot.format(dislikes, Colour.fg_red),
                                    bot.format(thumbnail, Colour.fg_grey))

    def on_message(self, bot, msg, reply):
        match = re.findall(REGEX, msg["message"], re.IGNORECASE)
        for i, video_id in enumerate(match):
            url = "https://www.googleapis.com/youtube/v3/videos"
            headers = {"User-Agent": "SmartBot"}
            payload = {
                "key": self.key,
                "id": video_id,
                "part": ",".join(["contentDetails", "snippet", "statistics"]),
            }

            res = requests.get(url, headers=headers, params=payload).json()
            if res["items"]:
                video = res["items"][0]
                reply(self._get_reply(bot, i, video))

    def on_help(self):
        return "Sends information about YouTube URLs posted."
