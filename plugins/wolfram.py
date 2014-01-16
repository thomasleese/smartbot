import lxml.etree
import re
import requests
import urllib.parse

class Plugin:
    def __init__(self, appid):
        self.appid = appid

    def __call__(self, bot):
        bot.on_respond(r"(?:\?|q|question|wfa|calc|calculate) (.*)$", self.on_respond)
        bot.on_hear(r"^\? (.*)$", self.on_respond)
        bot.on_help("wolfram", self.on_help)

    def format_pod(self, pod):
        subpod = pod.find("subpod")
        return self.format_subpod(subpod)

    def format_subpod(self, subpod):
        text = (subpod.find("plaintext").text or "").strip()
        if len(text) <= 0 or len(text) >= 400:
            return subpod.find("img").get("src")

        s = text

        # first convert unicode characters
        s = re.sub(r"\:([A-Za-z0-9]+)", lambda m: chr(int(m.group(), 16)), s)

        # then turn it into a table... if it is one
        if "|" in s:
            rows = s.splitlines()
            max_column_widths = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

            def format_row(row):
                def format_col(arg):
                    i = arg[0]
                    col = arg[1].strip()
                    if len(col) > max_column_widths[i]:
                        max_column_widths[i] = len(col)
                    return col

                return list(map(format_col, enumerate(row.split("|"))))

            rows = list(map(format_row, rows)) # list to force max_column_widths evaluation

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

    def on_respond(self, bot, msg, reply):
        url = "http://api.wolframalpha.com/v2/query?input={0}&appid={1}".format(
            urllib.parse.quote(msg["match"][0]),
            urllib.parse.quote(self.appid)
        )
        headers = { "User-Agent": "SmartBot" }

        page = requests.get(url, headers=headers, timeout=15)
        if page.status_code == 200:
            tree = lxml.etree.fromstring(page.content)
            pods = []
            for pod in tree.xpath("//pod"):
                pods.append(pod)

            small_result = self.format_pod(pods[0]) + " -> " + self.format_pod(pods[1])
            if len(small_result) <= 100 and "\n" not in small_result:
                reply(small_result)
            else:
                for pod in pods[:2]:
                    reply("# {0}".format(pod.get("title")))
                    for subpod in pod.findall("subpod"):
                        if subpod.get("title"):
                            reply("## {0}".format(subpod.get("title")))
                        reply(self.format_subpod(subpod))

    def on_help(self, bot, msg, reply):
        reply("Syntax: ?|q|question|wfa|calc|calculate <query>")
