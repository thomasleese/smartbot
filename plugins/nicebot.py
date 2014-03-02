import unittest


class Plugin:
    def __init__(self, nicebots):
        self.nicebots = nicebots

    def on_join(self, bot, msg):
        for nicebot in self.nicebots:
            if nicebot["channel"] == msg["channel"] and msg["is_me"]:
                bot.send(nicebot["target"], nicebot["password"])

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
        self.plugin = Plugin([{"channel": "#test", "target": "NiceBot", "password": "password"}])

    def test_join(self):
        self.plugin.on_join(Test.ExampleBot(self), {"channel": "#test", "is_me": True})

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
