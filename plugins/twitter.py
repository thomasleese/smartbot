import twython

class Plugin:
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        self.twitter = twython.Twython(consumer_key, consumer_secret, access_token, access_secret)

    def __call__(self, bot):
        bot.on_respond(r"twitter (.*)$", self.on_respond)
        bot.on_help("twitter", self.on_help)

    def on_respond(self, bot, msg, reply):
        tweets = self.twitter.get_user_timeline(screen_name=msg["match"][0])
        for i, tweet in enumerate(tweets[:3]):
            reply("[{0}]: {1}".format(i, tweet["text"]))

    def on_help(self, bot, msg, reply):
        reply("Syntax: twitter <person>")
