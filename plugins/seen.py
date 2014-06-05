import datetime

import smartbot


class Plugin(smartbot.Plugin):
    names = ["seen"]

    def on_message(self, msg, reply):
        self.bot.storage["seen." + msg["sender"]] = {
            "action": "spoke",
            "datetime": datetime.datetime.now()
        }

    def on_command(self, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            user = msg["args"][1]
            try:
                info = self.bot.storage["seen." + user]
                datetime_str = info["datetime"].strftime("%a %d %b %H:%M %Z").strip()
                print("{0} {1} on {2}.".format(user, info["action"], datetime_str), file=stdout)
            except KeyError:
                print("I don't know anything about {0}.".format(user), file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: seen <user>"
