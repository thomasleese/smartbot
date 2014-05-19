import io
import re
import unittest

from smartbot import utils


class Plugin:
    names = ["pastebin.com", "badpastebin"]

    def on_command(self, bot, msg, stdin, stdout, reply):
        arg0 = msg["args"][0]
        if arg0 == "pastebin.com":
            reply("Don't use it. Use some sane pastebin like bpaste.net, gist.github.com, sprunge.us or ix.io. Also see !badpastebin")
        elif arg0 == "badpastebin":
            reply("Ads, Spamfilters, Captcha, Adds whitespace, Slow, Ugly, No comment/fork/annotate, Breaks copy/paste, Blocked for some people, etc. See !pastebin.com")

    def on_help(self):
        return "Usage: pastebin.com|badpastebin"
