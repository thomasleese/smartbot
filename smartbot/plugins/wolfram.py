import io
import re

import lxml.etree

import smartbot.plugin
from smartbot.utils.web import requests_session
from smartbot.exceptions import StopCommand, StopCommandWithHelp
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Perform a wolfram request."""
    names = ["wolfram", "?"]

    def __init__(self, appid):
        self.appid = appid

    def format_pod(self, pod):
        subpod = pod.find("subpod")
        return self.format_subpod(subpod)

    def convert_unicode_chars(self, text):
        def filter(match):
            try:
                return chr(int(match.group(), 16))
            except ValueError:
                return match.group()

        return re.sub(r"\:([A-Za-z0-9]+)", filter, text)

    def format_subpod(self, subpod):
        text = (subpod.find("plaintext").text or "").strip()
        if len(text) <= 0:
            return subpod.find("img").get("src")

        s = text
        if len(s) >= 400:
            s = text[:400] + "…"

        # first convert unicode characters
        s = self.convert_unicode_chars(s)

        # then turn it into a table... if it is one
        if "|" in s:
            rows = s.splitlines()
            max_column_widths = [0] * 128

            def format_row(row):
                def format_col(arg):
                    i = arg[0]
                    col = arg[1].strip()

                    if len(col) > max_column_widths[i]:
                        max_column_widths[i] = len(col)

                    return col

                return list(map(format_col, enumerate(row.split("|"))))

            # force max_column_widths evaluation
            rows = list(map(format_row, rows))

            result = ""
            for row in rows:
                result += "|"
                for i, col in enumerate(row):
                    result += " " + col
                    result += " " * (max_column_widths[i] + 2 - len(col))
                    result += "|"
                result += "\n"
            return result.strip()
        else:
            return s.strip()

    def on_message(self, msg):
        if msg["message"].startswith("? "):
            query = msg["message"][2:]
            stdout = io.StringIO()
            self.on_command({"args": [None, query]}, None, stdout, None)
            output = stdout.getvalue().strip()
            self.bot.send(msg['reply_to'], output)

    def on_command(self, msg, stdin, stdout):
        query = " ".join(msg["args"][1:])
        if not query:
            query = stdin.read().strip()

        if query:
            url = "http://api.wolframalpha.com/v2/query"
            payload = {
                "input": query,
                "appid": self.appid,
            }

            session = requests_session()
            page = session.get(url, params=payload, timeout=15)
            if page.status_code == 200:
                tree = lxml.etree.fromstring(page.content)
                pods = []
                for pod in tree.xpath("//pod"):
                    pods.append(pod)

                if len(pods) >= 2:
                    small_result = '{} -> {}'.format(self.format_pod(pods[0]),
                                                     self.format_pod(pods[1]))
                    if len(small_result) <= 100 and "\n" not in small_result:
                        print(small_result, file=stdout)
                    else:
                        for pod in pods[:2]:
                            print("# {0}".format(pod.get("title")),
                                  file=stdout)
                            for subpod in pod.findall("subpod"):
                                if subpod.get("title"):
                                    print("## {0}".format(subpod.get("title")),
                                          file=stdout)
                                print(self.format_subpod(subpod), file=stdout)
                else:
                    raise StopCommand("Nothing more to say.")
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{} {}".format(
            super().on_help(),
            self.bot.format("query", Style.underline)
        )
