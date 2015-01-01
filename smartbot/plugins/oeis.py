import re

import smartbot.plugin
from smartbot.utils.web import requests_session
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Interface to OEIS."""
    names = ["oeis"]
    limit = 5

    def on_command(self, msg, stdin, stdout, reply):
        session = requests_session()
        url = "http://oeis.org/search"
        payload = {
            "fmt": "text",
            "q": " ".join(msg["args"][1:]),
        }

        response = session.get(url, params=payload)
        if response.status_code == 200:
            self.i = -1
            # only process lines starting with a percent symbol
            for line in filter(lambda l: l.startswith("%"),
                               response.text.split("\n")):
                # content default is set to None
                flag, identifier, content, *_ = line.split(" ", 2) + [None]
                # process the line
                self.process(flag, identifier, content, stdout)
                # stop when limit is reached
                if self.i >= self.limit:
                    print("...", file=stdout)
                    break

    def process(self, flag, identifier, content, stdout):
        # increase the sequence number
        if flag[1] == "I":
            self.i += 1
        # print formatted sequence
        elif flag[1] == "S":
            sequence = re.sub(",", ", ", content)
            print("[{}] {}: {}...".format(self.i, identifier, sequence),
                  file=stdout)
        # print sequence name
        elif flag[1] == "N":
            print(content, file=stdout)

    def on_help(self):
        return "{} {}   (see https://oeis.org/hints.html)".format(
            self.bot.format("oeis", Style.bold),
            self.bot.format("query", Style.underline),
        )
