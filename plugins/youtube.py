import re
import urllib

import isodate
import requests

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


REGEX = r"(https?://)?(www\.)?(youtu\.?be|listenonrepeat)(\.com)?([^\s]+)"

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
            self.bot.format(title, Style.underline),
            self.bot.format(channelTitle, Style.underline),
            duration,
            views,
            self.bot.format(likes, Colour.fg_green),
            self.bot.format(dislikes, Colour.fg_red)
        )

    def _find_video_ids(self, text):
        video_ids = []
        matches = re.findall(REGEX, text, re.IGNORECASE)
        for match in matches:
            try:
                url = urllib.parse.urlparse("".join(match))
                if url.netloc == "youtu.be":
                    video_ids.append(url.path[1:])
                else:
                    video_ids.extend(urllib.parse.parse_qs(url.query)["v"])
            except (ValueError, KeyError):
                pass
        return video_ids

    def pre_on_message(self, handler, msg):
        if self._find_video_ids(msg["message"]):
            handler.disable_plugin("websites")

    def _get_video_info(self, video_id):
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
            return video
        else:
            return None

    def on_message(self, msg, reply):
        video_ids = self._find_video_ids(msg["message"])
        for i, video_id in enumerate(video_ids):
            video = self._get_video_info(video_id)
            if video:
                reply(self._get_reply(i, video))

    def on_command(self, msg, stdin, stdout, reply):
        video_ids = msg["args"][1:]
        for i, video_id in enumerate(video_ids):
            video = self._get_video_info(video_id)
            if video:
                print(self._get_reply(i, video), file=stdout)

    def on_help(self):
        return "{} {} …".format(
            super().on_help(),
            self.bot.format("id", Style.underline)
        )
