import base64
import sys


class Plugin:
    def get_hash_func(self, algorithm, action):
        if algorithm == "base64" or algorithm == "b64":
            if action == "encode":
                return base64.b64encode
            elif action == "decode":
                return base64.b64decode
        elif algorithm == "base32" or algorithm == "b32":
            if action == "encode":
                return base64.b32encode
            elif action == "decode":
                return base64.b32decode
        elif algorithm == "base16" or algorithm == "b16":
            if action == "encode":
                return base64.b16encode
            elif action == "decode":
                return base64.b16decode

    def on_command(self, bot, msg):
        if len(sys.argv) >= 3:
            algorithm = sys.argv[1]
            action = sys.argv[2]
            contents = " ".join(sys.argv[3:])
            if not contents:
                contents = sys.stdin.read().strip()

            func = self.get_hash_func(algorithm, action)
            if func:
                result = str(func(bytes(contents, "utf-8")), "utf-8")
                print(result)
            else:
                print("No hash algorithm:", algorithm)
        else:
            print(self.on_help())

    def on_help(self):
        return "Usage: crypto <algorithm> encode|decode <contents>"
