import datetime
import re
import urllib

import isodate
import requests

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


REGEX = r"(https?://)?(www\.)?(vimeo\.com)([^\s]+)"

class Plugin(smartbot.Plugin):
    """Get information about posted Vimeo videos."""
    names = ["vimeo"]

    def _get_reply(self, i, video):
        title = video["title"]
        userName = video["user_name"]
        duration = datetime.timedelta(seconds=video["duration"])
        views = video["stats_number_of_plays"]
        likes = video["stats_number_of_likes"]

        return "{}: {} by {} | {} | {} {}".format(
            self.bot.format("[{}]".format(i), Style.bold),
            self.bot.format(title, Style.underline),
            self.bot.format(userName, Style.underline),
            duration,
            views,
            self.bot.format(likes, Colour.fg_green),
        )

    def _find_video_ids(self, text):
        video_ids = []
        matches = re.findall(REGEX, text, re.IGNORECASE)
        for match in matches:
            try:
                url = urllib.parse.urlparse("".join(match))
                video_ids.append(url.path[1:])
            except (ValueError, KeyError):
                pass
        return video_ids

    def pre_on_message(self, handler, msg):
        if self._find_video_ids(msg["message"]):
            handler.disable_plugin("websites")

    def _get_video_info(self, video_id):
        url = "http://vimeo.com/api/v2/video/{}.json".format(video_id)

        s = utils.web.requests_session()
        res = s.get(url).json()
        try:
            return res[0]
        except IndexError:
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
