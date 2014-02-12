import sys


class Plugin:
    def on_command(self, bot, msg):
        plugin_name = None
        if len(sys.argv) >= 2:
            plugin_name = sys.argv[1]
        else:
            plugin_name = sys.stdin.read().strip()

        if plugin_name:
            try:
                plugin = bot.plugins[plugin_name]
                print(plugin.on_help(bot))
            except KeyError:
                print("No such plugin:", plugin_name)
            except Exception as e:
                print(e)
        else:
            plugin_names = ", ".join([name for name, _ in bot.plugins.items()])
            print("Help about:", plugin_names)

    def on_help(self, bot):
        return "Usage: man [<plugin>]"
