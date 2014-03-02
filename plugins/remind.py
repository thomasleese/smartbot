import datetime
import io
import re
import time
import threading
import unittest

from smartbot import utils


class Plugin:
    def on_timeout(self, message, duration, reply):
        time.sleep(duration)
        reply(message)

    def on_command(self, bot, msg, stdin, stdout, reply):
        match = re.match(r"remind me (to|about|that) (.*) (in|at) (.*)$", msg["message"], re.IGNORECASE)
        if not match:
            match = re.match(r"remind me (to|about|that) (.*) (in|at) (.*)$", stdin.getvalue().strip(), re.IGNORECASE)

        if match:
            try:
                date = utils.datetime.parse("{0} {1}".format(match.group(3), match.group(4)))
            except ValueError:
                print("I don't understand that date.", file=stdout)
            else:
                print("Sure thing {0}, I'll remind you on {1}.".format(msg["sender"], date.strftime("%c")), file=stdout)
                message = "{0}: you asked me to remind you {1} {2}".format(msg["sender"], match.group(1), match.group(2))

                duration = max(0, (date - datetime.datetime.now()).total_seconds())
                t = threading.Thread(target=self.on_timeout, args=(message, duration, reply))
                t.start()

    def on_help(self):
        return "Usage: remind me to|about|that <something> in|at <time>"


class Test(unittest.TestCase):
    class ExampleBot:
        def __init__(self, test):
            self.test = test
            self.start_time = datetime.datetime.now()

        def send(self, target, message):
            self.test.assertIs(target, None)
            self.test.assertEqual(int((datetime.datetime.now() - self.start_time).total_seconds()), 2)

    def setUp(self):
        self.plugin = Plugin()

    def test_remind(self):
        stdout = io.StringIO()
        bot = Test.ExampleBot(self)
        msg = {"message": "remind me to do something in 2 seconds", "sender": "test"}
        self.plugin.on_command(bot, msg, None, stdout, lambda x: bot.send(None, x))
        self.assertNotEqual("I don't understand that date.", stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
