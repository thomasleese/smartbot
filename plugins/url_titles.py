import re
import urllib

import isodate

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


class YouTube:
    REGEX = r"(https?://)?(www\.)?(youtu\.?be|listenonrepeat)(\.com)?([^\s]+)"

    def __init__(self, key):
        self.key = key

    @staticmethod
    def _get_video_id(text):
        matches = re.findall(YouTube.REGEX, text, re.IGNORECASE)
        for match in matches:
            try:
                url = urllib.parse.urlparse("".join(match))
                if url.netloc == "youtu.be":
                    return url.path[1:]
                elif "v" in url.query:
                    return urllib.parse.parse_qs(url.query)["v"]
            except (ValueError, KeyError):
                pass

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

    @staticmethod
    def _get_title(bot, video):
        title = video["snippet"]["title"]
        channelTitle = video["snippet"]["channelTitle"]
        duration = isodate.parse_duration(video["contentDetails"]["duration"])
        views = video["statistics"]["viewCount"]
        likes = video["statistics"]["likeCount"]
        dislikes = video["statistics"]["dislikeCount"]

        return "{} by {} | {} | {} {} {}".format(
            bot.format(title, Style.underline),
            bot.format(channelTitle, Style.underline),
            duration,
            views,
            bot.format(likes, Colour.fg_green),
            bot.format(dislikes, Colour.fg_red)
        )

    def __call__(self, plugin, url):
        video_id = self._get_video_id(url)
        if video_id:
            video = self._get_video_info(video_id)
            if video:
                return self._get_title(plugin.bot, video)


class Website:
    def __call__(self, plugin, url):
        return utils.web.get_title(url)


class Plugin(smartbot.Plugin):
    """Get URL titles."""
    names = ["url_titles"]

    def __init__(self, youtube_key=None):
        self.handlers = []
        if youtube_key:
            self.handlers.append(YouTube(youtube_key))
        self.handlers.append(Website())

    def _get_title(self, url):
        for handler in self.handlers:
            title = handler(self, url)
            if title:
                return title

    def on_message(self, msg, reply):
        match = re.findall(r"(https?://[^\s]+)", msg["message"], re.IGNORECASE)
        for i, url in enumerate(match):
            title = self._get_title(url)
            if title:
                reply("{}: {}".format(
                    self.bot.format("[{}]".format(i), Style.bold),
                    title
                ))

    def on_help(self):
        return "Echos the title of any website URL."
