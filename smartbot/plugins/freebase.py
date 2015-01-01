import smartbot.plugin
from smartbot.utils.web import requests_session, sprunge
from smartbot.exceptions import StopCommand, StopCommandWithHelp
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """A plugin for searching Freebase."""
    names = ["define", "freebase"]

    def __init__(self, key):
        self.key = key

    def _search_mid(self, query):
        url = "https://www.googleapis.com/freebase/v1/search"
        payload = {
            "query": query,
            "key": self.key,
            "limit": 1
        }

        session = requests_session()
        res = session.get(url, params=payload).json()
        if res["result"]:
            return res["result"][0]["mid"]

    def _topic(self, mid):
        url = "https://www.googleapis.com/freebase/v1/topic{}".format(mid)
        session = requests_session()
        return session.get(url).json()

    def _look_for_text(self, topic):
        description = topic["property"].get("/common/topic/description")
        if description:
            return description["values"][0]["text"], \
                description["values"][0]["value"]
        else:
            return None, None

    def on_command(self, msg, stdin, stdout, reply):
        query = " ".join(msg["args"][1:])
        if not query:
            query = stdin.read().strip()

        if query:
            mid = self._search_mid(query)
            if mid:
                topic = self._topic(mid)
                short_text, long_text = self._look_for_text(topic)
                if short_text and long_text:
                    url = sprunge(long_text)
                    print("{} {}".format(short_text, url), file=stdout)
                else:
                    raise StopCommand(
                        "There isn't much information about this.")
            else:
                raise StopCommand("I don't know what you're on about.")
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{}|{} {}".format(
            self.bot.format("define", Style.bold),
            self.bot.format("freebase", Style.bold),
            self.bot.format("topic", Style.underline),
        )
