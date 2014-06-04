import io
import pprint

import requests

from smartbot import utils

class Plugin:
    names = ["define", "freebase"]

    def __init__(self, key):
        self.key = key

    def _search_mid(self, query):
        url = "https://www.googleapis.com/freebase/v1/search"
        headers = {"User-Agent": "SmartBot"}
        payload = {
            "query": query,
            "key": self.key,
            "limit": 1
        }

        res = requests.get(url, headers=headers, params=payload).json()
        if res["result"]:
            return res["result"][0]["mid"]
        else:
            return None

    def _topic(self, mid):
        url = "https://www.googleapis.com/freebase/v1/topic{}".format(mid)
        headers = {"User-Agent": "SmartBot"}

        res = requests.get(url, headers=headers).json()
        return res

    def _look_for_text(self, topic):
        description = topic["property"].get("/common/topic/description")
        if description:
            return description["values"][0]["text"], \
                   description["values"][0]["value"]
        else:
            return None, None

    def on_command(self, bot, msg, stdin, stdout, reply):
        query = " ".join(msg["args"][1:])
        if not query:
            query = stdin.read().strip()

        if query:
            mid = self._search_mid(query)
            if mid:
                topic = self._topic(mid)
                short_text, long_text = self._look_for_text(topic)
                if short_text and long_text:
                    url = utils.web.sprunge(long_text)
                    print("{} {}".format(short_text, url), file=stdout)
                else:
                    print("There isn't much information about this.", file=stdout)
            else:
                print("I don't know what you're on about.", file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: define|freebase <topic>"
