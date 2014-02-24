import twython
import sys



class Plugin:
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        self.twitter = twython.Twython(consumer_key, consumer_secret, access_token, access_secret)

    def on_command(self, bot, msg):
        person = None
        if len(sys.argv) >= 2:
            person = sys.argv[1]
        else:
            person = sys.stdin.read().strip()

        if person:
            tweets = self.twitter.get_user_timeline(screen_name=person)
            for i, tweet in enumerate(tweets[:3]):
                print("[{0}]: {1}".format(i, tweet["text"]))
        else:
            print(self.on_help())

    def on_help(self):
        return "Usage: twitter <person>"
