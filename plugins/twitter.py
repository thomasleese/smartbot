import io
import twython
import os
import unittest


class Plugin:
    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.twitter = twython.Twython(consumer_key, consumer_secret, access_token_key, access_token_secret)

    def on_command(self, bot, msg, stdin, stdout, reply):
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


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin(os.environ["TWITTER_CONSUMER_KEY"],
                             os.environ["TWITTER_CONSUMER_SECRET"],
                             os.environ["TWITTER_ACCESS_TOKEN_KEY"],
                             os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

    def test_command(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "tomleese"]}, None, stdout, None)
        self.assertEqual(len(stdout.getvalue().strip().splitlines()), 3)

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
