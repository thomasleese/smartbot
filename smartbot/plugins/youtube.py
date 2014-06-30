import re
import urllib

import isodate
import requests

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


REGEX = r"(?:https?://)?(?:www\.)?(?:youtu\.?be|listenonrepeat)(?:\.com)?/(?:watch/?\?v=)?([^\s]+)"

class Plugin(smartbot.Plugin):
    """Get information about posted YouTube videos."""
    names = ["youtube", "utube"]

    def __init__(self, key):
        self.key = key

    def _get_reply(self, i, video):
        title = video["snippet"]["title"]
        channelTitle = video["snippet"]["channelTitle"]
        duration = isodate.parse_duration(video["contentDetails"]["duration"])
        views = video["statistics"]["viewCount"]
        likes = video["statistics"]["likeCount"]
        dislikes = video["statistics"]["dislikeCount"]
        thumbnail = video["snippet"]["thumbnails"]["default"]["url"]

        return "{}: {} by {} | {} | {} {} {}".format(
            self.bot.format("[{}]".format(i), Style.bold),
            title,
            channelTitle,
            duration,
            views,
            self.bot.format(likes, Colour.fg_green),
            self.bot.format(dislikes, Colour.fg_red)
        )

    def pre_on_message(self, handler, msg):
        handler.disable_plugin("websites")

    def on_message(self, msg, reply):
        match = re.findall(REGEX, msg["message"], re.IGNORECASE)
        for i, video_id in enumerate(match):
            url = "https://www.googleapis.com/youtube/v3/videos"
            payload = {
                "key": self.key,
                "id": video_id,
                "part": ",".join(["contentDetails", "snippet", "statistics"])
            }

            s = utils.web.requests_session()
            res = s.get(url, params=payload).json()
            if res["items"]:
                video = res["items"][0]
                reply(self._get_reply(i, video))

    def on_help(self):
        return "Sends information about YouTube URLs posted."
