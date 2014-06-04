import io
import pprint

import requests


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
        for key, value in topic.get("property", {}).items():
            if key == "/common/document/text":
                return value["values"][0]["value"]
            else:
                for v in value["values"]:
                    text = self._look_for_text(v)
                    if text:
                        return text

    def on_command(self, bot, msg, stdin, stdout, reply):
        query = " ".join(msg["args"][1:])
        if not query:
            query = stdin.read().strip()

        if query:
            mid = self._search_mid(query)
            if mid:
                topic = self._topic(mid)
                text = self._look_for_text(topic)
                if text:
                    print(text)
                else:
                    print("There isn't much information about this", file=stdout)
            else:
                print("I don't know what you're on about.", file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: define|freebase <topic>"
