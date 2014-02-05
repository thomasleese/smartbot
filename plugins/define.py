import urllib.parse
import sys

import requests


class Plugin:
    def on_command(self, bot, msg):
        topic = " ".join(sys.argv[1:])
        if not topic:
            topic = sys.stdin.read().strip()

        if not topic:
            print(self.on_help(bot))
            return

        url = "http://api.duckduckgo.com/?format=json&q={0}".format(urllib.parse.quote(topic))
        headers = {"User-Agent": "SmartBot"}

        res = requests.get(url, headers=headers).json()
        if res.get("AbstractText"):
            print(res["AbstractText"])
            if res.get("AbstractURL"):
                print(res["AbstractURL"])
        elif res.get("RelatedTopics"):
            topic = res["RelatedTopics"][0]
            print(topic["Text"])
            if topic.get("FirstURL"):
                print(topic["FirstURL"])
        elif res.get("Definition"):
            print(res["Definition"])
            if res.get("DefinitionURL"):
                print(res["DefinitionURL"])
        else:
            print("Don't know what you're talking about.")

    def on_help(self, bot):
        return "Usage: define <topic>"
