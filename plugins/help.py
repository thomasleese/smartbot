import itertools

import smartbot
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Get help information about loaded plugins."""
    names = ["help", "what?"]

    def on_command(self, msg, stdin, stdout, reply):
        plugin_name = None
        if len(msg["args"]) >= 2:
            plugin_name = msg["args"][1]
        else:
            plugin_name = stdin.read().strip()

        if plugin_name:
            plugin = self.bot.find_plugin(plugin_name)
            if plugin:
                print(plugin.on_help(), file=stdout)
            else:
                raise StopCommand("{} does not exist.".format(plugin_name))
        else:
            plugin_names = ", ".join(sorted(itertools.chain.from_iterable(plugin.names for plugin in self.bot.plugins)))
            print("Help about:", plugin_names, file=stdout)

    def on_help(self):
        return "{} [{}]".format(
            self.bot.format("help", Style.bold),
            self.bot.format("plugin", Style.underline)
        )
