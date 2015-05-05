import datetime

import smartbot.plugin
from smartbot.utils.web import requests_session
from smartbot.formatting import Colour, Style


REGEX = r"(https?://)?(www\.)?(vimeo\.com)([^\s]+)"


class Plugin(smartbot.plugin.Plugin):
    """Get information about posted Vimeo videos."""
    names = ["vimeo"]

    def _get_reply(self, video):
        title = video["title"]
        userName = video["user_name"]
        duration = datetime.timedelta(seconds=video["duration"])
        views = video["stats_number_of_plays"]
        likes = video["stats_number_of_likes"]

        return "{} by {} | {} | {} {}".format(
            self.bot.format(title, Style.underline),
            self.bot.format(userName, Style.underline),
            duration,
            views,
            self.bot.format(likes, Colour.fg_green),
        )

    def _get_video_info(self, video_id):
        url = "http://vimeo.com/api/v2/video/{}.json".format(video_id)

        s = requests_session()
        res = s.get(url).json()
        try:
            return res[0]
        except IndexError:
            return None

    def on_command(self, msg, stdin, stdout):
        video_ids = msg["args"][1:]
        for i, video_id in enumerate(video_ids):
            video = self._get_video_info(video_id)
            if video:
                print(self._get_reply(video), file=stdout)

    def on_help(self):
        return "{} {} …".format(
            super().on_help(),
            self.bot.format("id", Style.underline)
        )
