from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin:
    STATUS_URL = "https://status.github.com/api/last-message.json"

    def on_command(self, bot, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            action = msg["args"][1]
            if "status".startswith(action):
                session = utils.web.requests_session()
                res = session.get(Plugin.STATUS_URL).json()
                print("{0} - {1}".format(res["created_on"], res["body"]), file=stdout)
            else:
                raise StopCommandWithHelp(self)
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{} status".format(self.bot.format("github", Style.bold))
