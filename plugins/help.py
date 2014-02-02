class Plugin:
    def on_command(self, bot, stdin, stdout, args):
        plugin_name = None
        if len(args) > 0:
            plugin_name = args[0]
        else:
            plugin_name = stdin.read().strip()

        if plugin_name:
            try:
                plugin = bot.plugins[plugin_name]
                print(plugin.on_help(bot), file=stdout)
            except KeyError:
                print("No such plugin:", plugin_name, file=stdout)
            except Exception as e:
                print(e, file=stdout)
        else:
            plugin_names = ", ".join([name for name, _ in bot.plugins.items()])
            print("Help about:", plugin_names, file=stdout)

    def on_help(self, bot):
        return "Usage: help [<plugin>]"
