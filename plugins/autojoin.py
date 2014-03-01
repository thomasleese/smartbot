import unittest

class Plugin:
    def __init__(self, channels):
        self.channels = channels

    def on_ready(self, bot):
        for channel in self.channels:
            bot.join(channel)

    def on_help(self):
        return "Automatically joins channels when the bot connects."


class Test(unittest.TestCase):
    class ExampleBot:
        def __init__(self, test, channel):
            self.test = test
            self.channel = channel

        def join(self, channel):
            self.test.assertEqual(channel, self.channel)

    def setUp(self):
        self.plugin = Plugin(["#test"])

    def test_join(self):
        self.plugin.on_ready(Test.ExampleBot(self, "#test"))

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
