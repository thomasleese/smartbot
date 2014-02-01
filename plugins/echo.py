class Plugin:
    def on_command(self, bot, stdin, stdout, args):
        stdout.write(" ".join(args) + "\n")

    def on_help(self, bot, msg):
        bot.send(msg["reply_to"], "Usage: echo <string>")
