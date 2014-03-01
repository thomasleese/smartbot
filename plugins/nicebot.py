import unittest


class Plugin:
    def __init__(self, channel, password, target="NiceBot"):
        self.channel = channel
        self.password = password
        self.target = target

    def on_join(self, bot, msg):
        if self.channel == msg["channel"] and msg["is_me"]:
            bot.send(self.target, self.password)

    def on_help(self):
        return "Authenticate with NiceBot."


class Test(unittest.TestCase):
    class ExampleBot:
        def __init__(self, test):
            self.test = test

        def send(self, target, message):
            self.test.assertEqual("NiceBot", target)
            self.test.assertEqual("password", message)

    def setUp(self):
        self.plugin = Plugin("#test", "password")

    def test_join(self):
        self.plugin.on_join(Test.ExampleBot(self), {"channel": "#test", "is_me": True})

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
