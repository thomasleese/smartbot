import io
import unittest


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        plugin_name = None
        if len(msg["args"]) >= 2:
            plugin_name = msg["args"][1]
        else:
            plugin_name = stdin.read().strip()

        if plugin_name:
            try:
                plugin = bot.plugins[plugin_name]
                print(plugin.on_help(), file=stdout)
            except KeyError:
                print("No such plugin:", plugin_name, file=stdout)
            except Exception as e:
                print(e, file=stdout)
        else:
            plugin_names = ", ".join(sorted(bot.plugins.keys()))
            print("Help about:", plugin_names, file=stdout)

    def on_help(self):
        return "Usage: help [<plugin>]"


class Test(unittest.TestCase):
    class ExampleBot:
        def __init__(self):
            self.plugins = {"a": None, "b": None}

    def setUp(self):
        self.plugin = Plugin()

    def test_no_plugin(self):
        stdout = io.StringIO()
        self.plugin.on_command(Test.ExampleBot(), {"args": [None, "_"]}, None, stdout, None)
        self.assertEqual("No such plugin: _", stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(Test.ExampleBot(), {"args": [None]}, stdout, stdout, None)
        self.assertEqual("Help about: a, b", stdout.getvalue().strip())

        stdout = io.StringIO()
        self.plugin.on_command(Test.ExampleBot(), {"args": [None, None]}, stdout, stdout, None)
        self.assertEqual("Help about: a, b", stdout.getvalue().strip())
