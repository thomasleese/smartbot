import smartbot.plugin


class Plugin(smartbot.plugin.Plugin):
    """
    Argh, don't use Pastebin, please!

    Inspired by the bot in the #archlinux freenode channel.
    """
    names = ["pastebin.com", "badpastebin"]

    def on_command(self, msg, stdin, stdout, reply):
        arg0 = msg["args"][0]
        if arg0 == "pastebin.com":
            print("Don't use it. Use some sane pastebin like bpaste.net, gist.github.com, sprunge.us or ix.io. Also see !badpastebin", file=stdout)
        elif arg0 == "badpastebin":
            print("Ads, Spamfilters, Captcha, Adds whitespace, Slow, Ugly, No comment/fork/annotate, Breaks copy/paste, Blocked for some people, etc. See !pastebin.com", file=stdout)
