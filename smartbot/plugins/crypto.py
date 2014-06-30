import base64

import smartbot
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Provide crypto functions."""
    names = ["crypto"]

    @staticmethod
    def _get_hash_func(algorithm, action):
        if algorithm == "base64" or algorithm == "b64":
            if "encode".startswith(action):
                return base64.b64encode
            elif "decode".startswith(action):
                return base64.b64decode
        elif algorithm == "base32" or algorithm == "b32":
            if "encode".startswith(action):
                return base64.b32encode
            elif "decode".startswith(action):
                return base64.b32decode
        elif algorithm == "base16" or algorithm == "b16":
            if "encode".startswith(action):
                return base64.b16encode
            elif "decode".startswith(action):
                return base64.b16decode

        raise StopCommand("{} is not a valid algorithm.".format(algorithm))

    def on_command(self, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 3:
            algorithm = msg["args"][1]
            action = msg["args"][2]
            value = " ".join(msg["args"][3:])
            if not value:
                value = stdin.read().strip()

            if action not in ["encode", "decode"]:
                raise StopCommandWithHelp(self)

            if not value:
                raise StopCommandWithHelp(self)

            func = self._get_hash_func(algorithm, action)
            result = str(func(bytes(value, "utf-8")), "utf-8")
            print(result, file=stdout)
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{} {} encode|decode {}".format(
            self.bot.format("crypto", Style.bold),
            self.bot.format("algorithm", Style.underline),
            self.bot.format("value", Style.underline)
        )
