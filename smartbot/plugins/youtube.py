import isodate

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Get information about posted YouTube videos."""
    names = ["youtube", "utube"]

    def __init__(self, key):
        self.key = key

    def _get_reply(self, video):
        title = video["snippet"]["title"]
        channelTitle = video["snippet"]["channelTitle"]
        duration = isodate.parse_duration(video["contentDetails"]["duration"])
        views = video["statistics"]["viewCount"]
        likes = video["statistics"]["likeCount"]
        dislikes = video["statistics"]["dislikeCount"]

        return "{} by {} | {} | {} {} {}".format(
            self.bot.format(title, Style.underline),
            self.bot.format(channelTitle, Style.underline),
            duration,
            views,
            self.bot.format(likes, Colour.fg_green),
            self.bot.format(dislikes, Colour.fg_red)
        )

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
            return res["items"][0]

    def on_command(self, msg, stdin, stdout, reply):
        for video_id in msg["args"][1:]:
            video = self._get_video_info(video_id)
            if video:
                print(self._get_reply(video), file=stdout)

    def on_help(self):
        return "{} {} …".format(
            super().on_help(),
            self.bot.format("id", Style.underline)
        )
