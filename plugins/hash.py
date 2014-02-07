import hashlib
import sys


class Plugin:
    def on_command(self, bot, msg):
        if len(sys.argv) >= 2:
            algorithm = sys.argv[1]
            contents = " ".join(sys.argv[2:])
            if not contents:
                contents = sys.stdin.read().strip()

            h = hashlib.new(algorithm)
            h.update(bytes(contents, "utf-8"))
            print(h.hexdigest())
        else:
            print(self.on_help(bot))

    def on_help(self, bot):
        return "Usage: hash <algorithm> <contents>"
