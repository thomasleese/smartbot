import datetime
import re
import urllib

import isodate
import twython

import smartbot.plugin
from smartbot.utils.web import get_title, requests_session
from smartbot.formatting import Colour, Style


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

        s = requests_session()
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


class Vimeo:
    REGEX = r"(https?://)?(www\.)?(vimeo\.com)([^\s]+)"

    @staticmethod
    def _get_video_id(url):
        matches = re.findall(Vimeo.REGEX, url, re.IGNORECASE)
        for match in matches:
            try:
                url = urllib.parse.urlparse("".join(match))
                return url.path[1:]
            except (ValueError, KeyError):
                pass

    def _get_video_info(self, video_id):
        url = "http://vimeo.com/api/v2/video/{}.json".format(video_id)

        s = requests_session()
        res = s.get(url).json()
        try:
            return res[0]
        except IndexError:
            return None

    @staticmethod
    def _get_title(bot, video):
        title = video["title"]
        userName = video["user_name"]
        duration = datetime.timedelta(seconds=video["duration"])
        views = video["stats_number_of_plays"]
        likes = video["stats_number_of_likes"]

        return "{} by {} | {} | {} {}".format(
            bot.format(title, Style.underline),
            bot.format(userName, Style.underline),
            duration,
            views,
            bot.format(likes, Colour.fg_green),
        )

    def __call__(self, plugin, url):
        video_id = self._get_video_id(url)
        if video_id:
            video = self._get_video_info(video_id)
            if video:
                return self._get_title(plugin.bot, video)


class Instagram:
    REGEX = r"(https?://)?(www\.)?(instagram.com/p/[^\s]+)"

    def __init__(self, client_id):
        self.client_id = client_id

    @staticmethod
    def _get_title(bot, media):
        caption = media["caption"]["text"]
        userName = media["user"]["full_name"]
        likes = media["likes"]["count"]

        return "{} by {} | {}".format(
            bot.format(caption, Style.underline),
            bot.format(userName, Style.underline),
            bot.format(likes, Colour.fg_green),
        )

    @staticmethod
    def _get_shortcode(text):
        matches = re.findall(Instagram.REGEX, text, re.IGNORECASE)
        for match in matches:
            try:
                url = urllib.parse.urlparse("".join(match))
                return url.path.split("/")[2]
            except (ValueError, KeyError):
                pass

    def _get_media_info(self, shortcode):
        url = "https://api.instagram.com/v1/media/shortcode/{}" \
              .format(shortcode)
        params = {
            "client_id": self.client_id,
        }

        s = requests_session()
        res = s.get(url, params=params).json()
        try:
            return res["data"]
        except KeyError:
            return None

    def __call__(self, plugin, url):
        shortcode = self._get_shortcode(url)
        if shortcode:
            media = self._get_media_info(shortcode)
            if media:
                return self._get_title(plugin.bot, media)


class Twitter:
    REGEX = r"(?:https?://)?(?:www\.)?(?:twitter\.com)([^\s]+)/status/([0-9]+)"

    def __init__(self, consumer_key, consumer_secret, access_token_key,
                 access_token_secret):
        self.twitter = twython.Twython(consumer_key, consumer_secret,
                                       access_token_key, access_token_secret)

    @staticmethod
    def _get_status_id(text):
        matches = re.findall(Twitter.REGEX, text, re.IGNORECASE)
        for match in matches:
            return match[1]

    def __call__(self, plugin, url):
        status_id = self._get_status_id(url)
        if status_id is not None:
            status = self.twitter.show_status(id=status_id)
            return "{} {}".format(
                status["text"],
                plugin.bot.format("@" + status["user"]["screen_name"],
                                  Style.underline, Style.bold)
            )


class Twitch:
    REGEX = r"(https?://)?(www\.)?(twitch\.tv)([^\s]+)"

    @staticmethod
    def _get_channel_id(url):
        matches = re.findall(Twitch.REGEX, url, re.IGNORECASE)
        for match in matches:
            try:
                url = urllib.parse.urlparse("".join(match))
                return url.path[1:]
            except (ValueError, KeyError):
                pass

    def _get_channel_info(self, channel_id):
        url = "https://api.twitch.tv/kraken/channels/{}".format(channel_id)
        s = requests_session()
        res = s.get(url).json()
        if res.get("error", None) is None:
            return res

    @staticmethod
    def _get_title(bot, channel):
        title = channel["status"]
        userName = channel["display_name"]

        return "{} by {}".format(
            bot.format(title, Style.underline),
            bot.format(userName, Style.underline)
        )

    def __call__(self, plugin, url):
        channel_id = self._get_channel_id(url)
        if channel_id:
            channel = self._get_channel_info(channel_id)
            if channel:
                return self._get_title(plugin.bot, channel)


class Website:
    def __call__(self, plugin, url):
        return get_title(url)


class Plugin(smartbot.plugin.Plugin):
    """Get URL titles."""
    names = ["url_titles"]

    def __init__(self, youtube_key=None, instagram_client_id=None,
                 twitter_consumer_key=None, twitter_consumer_secret=None,
                 twitter_access_token_key=None,
                 twitter_access_token_secret=None):
        self.handlers = []
        if youtube_key:
            self.handlers.append(YouTube(youtube_key))
        if instagram_client_id:
            self.handlers.append(Instagram(instagram_client_id))
        if twitter_consumer_key and twitter_consumer_secret and \
                twitter_access_token_key and twitter_access_token_secret:
            self.handlers.append(Twitter(twitter_consumer_key,
                                         twitter_consumer_secret,
                                         twitter_access_token_key,
                                         twitter_access_token_secret))
        self.handlers.append(Vimeo())
        self.handlers.append(Twitch())
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
