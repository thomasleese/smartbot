import io
import itertools
import functools
import shlex
import sys
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
            if hasattr(plugin, "on_ready"):
                try:
                    plugin.on_ready(self)
                except:
                    traceback.print_exc()

    def on_join(self, msg):
        for name, plugin in self.plugins.items():
            if hasattr(plugin, "on_join"):
                try:
                    plugin.on_join(self, msg)
                except:
                    traceback.print_exc()

    def on_message(self, msg):
        reply = functools.partial(self.send, msg["reply_to"])

        for name, plugin in self.plugins.items():
            if hasattr(plugin, "on_message"):
                try:
                    plugin.on_message(self, msg, reply)
                except Exception as e:
                    traceback.print_exc()
                    reply(name + ": " + str(e))

        m = msg["message"]
        if m.startswith(self.name):
            m = m[len(self.name)+1:].strip()

            msg["message"] = m
            for name, plugin in self.plugins.items():
                if hasattr(plugin, "on_respond"):
                    try:
                        plugin.on_respond(self, msg, reply)
                    except Exception as e:
                        traceback.print_exc()
                        reply(name + ": " + str(e))

            args = shlex.split(m)
            commands = [list(group) for k, group in itertools.groupby(args, lambda x: x == "|") if not k]
            pipe_buffer = ""
            for command in commands:
                if command[0] not in self.plugins:
                    break

                plugin = self.plugins[command[0]]
                if not hasattr(plugin, "on_command"):
                    break

                old_stdin = sys.stdin
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                old_argv = sys.argv

                try:
                    sys.stdin = io.StringIO(pipe_buffer)
                    sys.stdout = io.StringIO()
                    sys.stderr = io.StringIO()
                    sys.argv = command
                    plugin.on_command(self, msg)
                    pipe_buffer = sys.stdout.getvalue()
                    self.send(msg["reply_to"], sys.stderr.getvalue())
                except Exception as e:
                    traceback.print_exc()
                    self.send(msg["reply_to"], str(e))
                    break
                finally:
                    sys.stdin = old_stdin
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr
                    sys.argv = old_argv
            else:
                self.send(msg["reply_to"], pipe_buffer.strip())

    # actions
    def join(self, channel):
        self.backend.join(channel)

    def send(self, target, message):
        self.backend.send(target, str(message))
