import twython

import smartbot


class Plugin(smartbot.Plugin):
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

        if person:
            tweets = self.twitter.get_user_timeline(screen_name=person)
            for i, tweet in enumerate(tweets[:3]):
                text = tweet["text"].replace("\n", " ").replace("\r", "").strip()
                print("[{0}]: {1}".format(i, text), file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: twitter <person>"
