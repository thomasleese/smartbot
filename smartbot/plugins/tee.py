import smartbot.plugin


class Plugin(smartbot.plugin.Plugin):
    """Copy stdin to a reply, while also to standard output."""
    names = ["tee"]

    def on_command(self, msg, stdin, stdout):
        text = stdin.read().strip()

        self.bot.send(msg['reply_to'], text)
        print(text, file=stdout)

    def on_help(self):
        return "Copy standard input to reply, and also to standard output."
