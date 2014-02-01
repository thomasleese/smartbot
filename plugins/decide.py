import shlex
import random


class Plugin:
    def on_command(self, bot, stdin, stdout, args):
        if len(args) == 0:
            args = shlex.split(stdin.read())
        stdout.write(random.choice(args) + "\n")
