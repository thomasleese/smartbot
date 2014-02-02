import io
import itertools
import shlex
import traceback


class Bot:
    def __init__(self, name):
        self.name = name
        self.storage = None
        self.backend = None
        self.plugins = {}

    def set_storage(self, storage):
        self.storage = storage

    def set_backend(self, backend):
        self.backend = backend
        self.backend.add_event_listener("ready", self.on_ready)
        self.backend.add_event_listener("join", self.on_join)
        self.backend.add_event_listener("message", self.on_message)

    def add_plugin(self, name, plugin):
        self.plugins[name] = plugin

    def set_plugins(self, plugins):
        self.plugins.clear()
        for plugin in plugins:
            self.add_plugin(*plugin)

    def run(self):
        self.backend.run(self.name)

    # event handlers
    def on_ready(self):
        for name, plugin in self.plugins.items():
            try:
                plugin.on_ready(self)
            except:
                pass

    def on_join(self, msg):
        for name, plugin in self.plugins.items():
            try:
                plugin.on_join(self, msg)
            except:
                traceback.print_exc()

    def on_message(self, msg):
        for name, plugin in self.plugins.items():
            if hasattr(plugin, "on_message"):
                try:
                    plugin.on_message(self, msg)
                except Exception as e:
                    traceback.print_exc()
                    self.send(msg["reply_to"], e)

        m = msg["message"]
        if m.startswith(self.name):
            args = shlex.split(m[len(self.name)+1:].strip())
            commands = [list(group) for k, group in itertools.groupby(args, lambda x: x == "|") if not k]
            pipe_buffer = ""
            for command in commands:
                try:
                    plugin = self.plugins[command[0]]
                    stdin = io.StringIO(pipe_buffer)
                    stdout = io.StringIO()
                    plugin.on_command(self, stdin, stdout, command[1:])
                    pipe_buffer = stdout.getvalue()
                except Exception as e:
                    traceback.print_exc()
                    self.send(msg["reply_to"], e)
                    break
            else:
                self.send(msg["reply_to"], pipe_buffer.strip())

    # actions
    def join(self, channel):
        self.backend.join(channel)

    def send(self, target, message):
        self.backend.send(target, str(message))
