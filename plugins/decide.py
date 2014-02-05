import random
import shlex
import sys

class Plugin:
    def on_command(self, bot, msg):
        args = sys.argv[1:]
        if not args:
            args = shlex.split(sys.stdin.read().strip())
        print(random.choice(args))

    def on_help(self, bot):
        return "Usage: decide <a> <b> ..."
