import datetime
import io
import unittest


class Plugin:
    def on_message(self, bot, msg, reply):
        bot.storage["seen." + msg["sender"]] = {
            "action": "spoke",
            "datetime": datetime.datetime.now()
        }

    def on_command(self, bot, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            user = msg["args"][1]
            try:
                info = bot.storage["seen." + user]
                datetime_str = info["datetime"].strftime("%a %d %b %H:%M %Z").strip()
                print("{0} {1} on {2}.".format(user, info["action"], datetime_str), file=stdout)
            except KeyError:
                print("I don't know anything about {0}.".format(user), file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: seen <user>"


class Test(unittest.TestCase):
    class ExampleBot:
        def __init__(self):
            self.storage = {}

    def setUp(self):
        self.plugin = Plugin()

    def test_message(self):
        bot = Test.ExampleBot()
        self.plugin.on_message(bot, {"sender": "test"}, None)
        self.assertIn("seen.test", bot.storage)

    def test_command(self):
        stdout = io.StringIO()
        bot = Test.ExampleBot()
        bot.storage["seen.test"] = {"action": "spoke", "datetime": datetime.datetime.now()}
        self.plugin.on_command(bot, {"args": [None, "test"]}, None, stdout, None)
        self.assertNotEqual("I don't know anything about test.", stdout.getvalue().strip())

        stdout = io.StringIO()
        self.plugin.on_command(bot, {"args": [None, "test2"]}, None, stdout, None)
        self.assertEqual("I don't know anything about test2.", stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
