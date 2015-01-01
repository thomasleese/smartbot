import smartbot.plugin
from smartbot.utils.web import requests_session
from smartbot.exceptions import StopCommandWithHelp
from smartbot.formatting import Style


STATUS_URL = "https://status.github.com/api/last-message.json"


class Plugin(smartbot.plugin.Plugin):
    """Get the status of GitHub."""
    names = ["github", "gh"]

    def on_command(self, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            action = msg["args"][1]
            if "status".startswith(action):
                session = requests_session()
                res = session.get(STATUS_URL).json()
                print("{0} - {1}".format(res["created_on"], res["body"]),
                      file=stdout)
            else:
                raise StopCommandWithHelp(self)
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{}|{} status".format(
            self.bot.format("github", Style.bold),
            self.bot.format("gh", Style.bold)
        )
