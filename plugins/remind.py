import datetime
import time
import threading

from smartbot import utils

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"remind me (to|about|that) (.*) (in|at) (.*)$", self.on_respond)
        bot.on_help("remind", self.on_help)

    def on_timeout(self, message, duration, reply):
        time.sleep(duration)
        reply(message)

    def on_respond(self, bot, msg, reply):
        try:
            match = msg["match"][0]
            date = utils.parse_datetime("{0} {1}".format(match[2], match[3]))
            reply("Sure thing {0}, I'll remind you at {1}.".format(msg["sender"], date))
            message = "{0}: you asked me to remind you {1} {2}".format(msg["sender"], match[0], match[1])
            duration = max(0, (date - datetime.datetime.now()).total_seconds())
            t = threading.Thread(target=self.on_timeout, args=( message, duration, reply ))
            t.start()
        except ValueError:
            reply("I don't understand that date.")

    def on_help(self, bot, msg, reply):
        reply("Syntax: remind me to|about|that <something> in|at <time>")
