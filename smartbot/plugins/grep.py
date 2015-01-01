import re

import smartbot.plugin
from smartbot.exceptions import StopCommandWithHelp
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Look for substrings or regular expressions in lines."""
    names = ["grep"]

    def on_command(self, msg, stdin, stdout, reply):
        pattern_str = " ".join(msg["args"][1:])
        if not pattern_str:
            raise StopCommandWithHelp(self)

        pattern = re.compile(pattern_str)
        for line in map(str.strip, stdin):
            if pattern_str in line or re.match(pattern, line):
                print(line, file=stdout)

    def on_help(self):
        return "{} {}".format(
            self.bot.format("grep", Style.bold),
            self.bot.format("pattern", Style.underline)
        )
