import smartbot


class Plugin(smartbot.Plugin):
    names = ["sendto"]

    def on_command(self, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            user = msg["args"][1]
            message = " ".join(msg["args"][2:])
            if not message:
                message = stdin.read().strip()

            print("{0}: {1}".format(user, message), file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: sendto <user> [<message>]"
