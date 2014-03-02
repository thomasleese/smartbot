import lxml.etree
import io
import re
import requests
import os
import unittest
import urllib.parse


class Plugin:
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

    def on_message(self, bot, msg, reply):
        if msg["message"].startswith("? "):
            query = msg["message"][2:]
            stdout = io.StringIO()
            self.on_command(bot, {"args": [None, query]}, None, stdout, None)  # stdin, reply is unused
            output = stdout.getvalue().strip()
            reply(output)

    def on_command(self, bot, msg, stdin, stdout, reply):
        query = " ".join(msg["args"][1:])
        if not query:
            query = stdin.read().strip()

        if query:
            url = "http://api.wolframalpha.com/v2/query?input={0}&appid={1}".format(
                urllib.parse.quote(query),
                urllib.parse.quote(self.appid)
            )
            headers = {"User-Agent": "SmartBot"}

            page = requests.get(url, headers=headers, timeout=15)
            if page.status_code == 200:
                tree = lxml.etree.fromstring(page.content)
                pods = []
                for pod in tree.xpath("//pod"):
                    pods.append(pod)

                if len(pods) >= 2:
                    small_result = self.format_pod(pods[0]) + " -> " + self.format_pod(pods[1])
                    if len(small_result) <= 100 and "\n" not in small_result:
                        print(small_result, file=stdout)
                    else:
                        for pod in pods[:2]:
                            print("# {0}".format(pod.get("title")), file=stdout)
                            for subpod in pod.findall("subpod"):
                                if subpod.get("title"):
                                    print("## {0}".format(subpod.get("title")), file=stdout)
                                print(self.format_subpod(subpod), file=stdout)
                else:
                    print("Nothing more to say.", file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: wolfram <query>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin(os.environ["WOLFRAM_APPID"])

    def test_command(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "2+2"]}, None, stdout, None)
        self.assertNotEqual("Nothing more to say.", stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
