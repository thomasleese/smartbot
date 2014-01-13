import urllib.parse
import requests

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"define (.+)$", self.on_respond)
        bot.on_help("define", self.on_help)

    def on_respond(self, bot, msg, reply):
        url = "http://api.duckduckgo.com/?format=json&q={0}".format(urllib.parse.quote(msg["match"][0]))
        headers = { "User-Agent": "SmartBot" }

        res = requests.get(url, headers=headers).json()
        if res.get("AbstractText"):
            reply(res["AbstractText"])
            if res.get("AbstractURL"):
                reply(res["AbstractURL"])
        elif len(res.get("RelatedTopics", [])) > 0:
            topic = res["RelatedTopics"][0]
            reply(topic["Text"])
            if topic.get("FirstURL"):
                reply(topic["FirstURL"])
        elif res.get("Definition"):
            reply(res["Definition"])
            if res.get("DefinitionURL"):
                reply(res["DefinitionURL"])
        else:
            reply("Don't know what you're talking about.")

    def on_help(self, bot, reply):
        reply("Syntax: define <topic>")
