import datetime
import sys


class Plugin:
    def on_message(self, bot, msg):
        bot.storage["seen." + msg["sender"]] = {
            "action": "spoke",
            "datetime": datetime.datetime.now()
        }

    def on_command(self, bot, msg):
        if len(sys.argv) >= 2:
            user = sys.argv[1]
            try:
                info = bot.storage["seen." + user]
                print("{0} {1} on {2}.".format(user, info["action"],
                                               info["datetime"].strftime("%a %d %b %H:%M %Z").strip()))
            except KeyError:
                print("I don't know anything about {0}.".format(user))
        else:
            print(self.on_help())

    def on_help(self):
        return "Usage: seen <user>"
