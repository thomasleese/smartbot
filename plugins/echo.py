class Plugin:
    def on_command(self, bot, stdin, stdout, args):
        print(*args, file=stdout)

    def on_help(self, bot):
        return "Usage: echo <string>"
