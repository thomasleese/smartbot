import sys


class Plugin:
    def on_command(self, bot, msg):
        print(*sys.argv[1:])

    def on_help(self):
        return "Usage: echo <string>"
