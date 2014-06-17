import datetime
import re
import time

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Remind me to do something."""
    names = ["remind"]

    def on_command(self, msg, stdin, stdout, reply):
        pattern_str = r"remind (me|[^\s]+) (to|about|that) (.*) (in|at) (.*)$"
        match = re.match(pattern_str, msg["message"], re.IGNORECASE)
        if not match:
            match = re.match(pattern_str, stdin.getvalue().strip(), re.IGNORECASE)

        if match:
            try:
                date = utils.datetime.parse("{0} {1}".format(match.group(4), match.group(5)))
            except ValueError:
                raise StopCommand("I don't understand that date.")
            else:
                message = None
                if match.group(1) == "me" or match.group(1) == msg["sender"]:
                    reply("Sure thing {0}, I'll remind you on {1}.".format(msg["sender"], date.strftime("%c").strip()))
                    message = "{0}: you asked me to remind you {1} {2}".format(msg["sender"], match.group(2), match.group(3))
                else:
                    replyreply("Sure thing {0}, I'll remind {1} on {2}.".format(msg["sender"], match.group(1), date.strftime("%c").strip()))
                    message = "{0}: {1} asked me to remind you {2} {3}".format(match.group(1), msg["sender"], match.group(2), match.group(3))

                duration = max(0, (date - datetime.datetime.now()).total_seconds())
                time.sleep(duration)
                print(message, file=stdout)

    def on_help(self):
        return "{} me|{} to|about|that {} in|at {}".format(
            super().on_help(),
            self.bot.format("target", Style.underline),
            self.bot.format("something", Style.underline),
            self.bot.format("time", Style.underline),
        )
