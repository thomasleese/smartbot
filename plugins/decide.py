import shlex
import random


class Plugin:
    def on_command(self, bot, stdin, stdout, args):
        if len(args) == 0:
            args = shlex.split(stdin.read().strip())
        print(random.choice(args), file=stdout)

    def on_help(self, bot):
        return "Usage: decide <a> <b> ..."
