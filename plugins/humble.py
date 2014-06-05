import lxml.html
import requests

import smartbot


class Plugin(smartbot.Plugin):
    names = ["humble", "humblebundle"]

    def on_command(self, msg, stdin, stdout, reply):
        url = "https://www.humblebundle.com/"
        if "weekly" in msg["args"] or "weekly" in stdin.read().strip():
            url = "https://www.humblebundle.com/weekly"

        page = requests.get(url)
        tree = lxml.html.fromstring(page.text)
        try:
            title = tree.cssselect("title")[0].text_content().strip()
            clock = tree.cssselect("#heading-time-remaining .mini-digit-holder")[0]
            c0 = clock.cssselect(".c0 .heading-num")[0].text_content()
            c1 = clock.cssselect(".c1 .heading-num")[0].text_content()
            c2 = clock.cssselect(".c2 .heading-num")[0].text_content()
            c3 = clock.cssselect(".c3 .heading-num")[0].text_content()
            c4 = clock.cssselect(".c4 .heading-num")[0].text_content()
            c5 = clock.cssselect(".c5 .heading-num")[0].text_content()
            c6 = clock.cssselect(".c6 .heading-num")[0].text_content()
            c7 = clock.cssselect(".c7 .heading-num")[0].text_content()
            print("{0} - {1}{2}:{3}{4}:{5}{6}:{7}{8} left".format(
                title, c0, c1, c2, c3, c4, c5, c6, c7
            ), file=stdout)
        except IndexError:
            print("No sale.", file=stdout)

    def on_help(self):
        return "Usage: humble [weekly]"
