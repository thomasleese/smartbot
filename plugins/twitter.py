import twython

import smartbot
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Get tweets from a user."""
    names = ["tweetie", "twitter"]

    def __init__(self, consumer_key, consumer_secret,
                 access_token_key, access_token_secret):
        self.twitter = twython.Twython(consumer_key, consumer_secret,
                                       access_token_key, access_token_secret)

    def on_command(self, msg, stdin, stdout, reply):
        person = None
        if len(msg["args"]) >= 2:
            person = msg["args"][1]
        else:
            person = stdin.read().strip()

        if not person:
            raise StopCommandWithHelp(self)

        tweets = self.twitter.get_user_timeline(screen_name=person)
        for i, tweet in enumerate(tweets[:3]):
            text = tweet["text"].replace("\n", " ").replace("\r", "").strip()
            print("[{0}]: {1}".format(i, text), file=stdout)

    def on_help(self):
        return "{} {}".format(
            super().on_help(),
            self.bot.format("person", Style.underline)
        )
