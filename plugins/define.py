import urllib.parse

import requests


class Plugin:
    def on_command(self, bot, stdin, stdout, args):
        topic = " ".join(args)
        if not topic:
            topic = stdin.read().strip()

        if not topic:
            print(self.on_help(bot), file=stdout)
            return

        url = "http://api.duckduckgo.com/?format=json&q={0}".format(urllib.parse.quote(topic))
        headers = {"User-Agent": "SmartBot"}

        res = requests.get(url, headers=headers).json()
        if res.get("AbstractText"):
            print(res["AbstractText"], file=stdout)
            if res.get("AbstractURL"):
                print(res["AbstractURL"], file=stdout)
        elif res.get("RelatedTopics"):
            topic = res["RelatedTopics"][0]
            print(topic["Text"], file=stdout)
            if topic.get("FirstURL"):
                print(topic["FirstURL"], file=stdout)
        elif res.get("Definition"):
            print(res["Definition"], file=stdout)
            if res.get("DefinitionURL"):
                print(res["DefinitionURL"], file=stdout)
        else:
            print("Don't know what you're talking about.", file=stdout)

    def on_help(self, bot):
        return "Usage: define <topic>"
