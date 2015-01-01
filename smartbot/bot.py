import io
import itertools
import functools
import shlex
import threading
import traceback

from .exceptions import StopCommand


class Bot:
    def __init__(self, name):
        self.name = name
        self.storage = None
        self.backend = None
        self.plugins = []

    def set_storage(self, storage):
        self.storage = storage

    def set_backend(self, backend):
        self.backend = backend
        self.backend.on_ready.register(self.on_ready)
        self.backend.on_join.register(self.on_join)
        self.backend.on_message.register(self.on_message)

    def add_plugin(self, plugin):
        self.plugins.append(plugin)
        plugin(self)

    def set_plugins(self, plugins):
        self.plugins.clear()
        for plugin in plugins:
            self.add_plugin(plugin)

    def run(self):
        self.backend.run(self.name)

    # event handlers
    def on_ready(self):
        for plugin in self.plugins:
            try:
                plugin.on_ready()
            except:
                traceback.print_exc()

    def on_join(self, msg):
        for plugin in self.plugins:
            try:
                plugin.on_join(msg)
            except:
                traceback.print_exc()

    def find_plugin(self, name):
        for plugin in self.plugins:
            if name in plugin.names:
                return plugin

    def call_plugins_on_message(self, msg):
        reply = functools.partial(self.send, msg["reply_to"])

        for plugin in self.plugins:
            try:
                plugin.on_message(msg, reply)
            except Exception as e:
                traceback.print_exc()
                reply(str(e))

    def call_plugins_on_respond(self, msg):
        reply = functools.partial(self.send, msg["reply_to"])

        for plugin in self.plugins:
            try:
                plugin.on_respond(msg, reply)
            except Exception as e:
                traceback.print_exc()
                reply(str(e))

    @staticmethod
    def _parse_message_into_commands(msg):
        try:
            args = shlex.split(msg["message"])
        except ValueError:
            args = msg["message"].split(" ")  # try and cope with invalid data

        groups = itertools.groupby(args, lambda x: x == "|")
        return [list(group) for k, group in groups if not k]

    def call_plugins_on_command(self, msg):
        reply = functools.partial(self.send, msg["reply_to"])
        commands = self._parse_message_into_commands(msg)
        pipe_buffer = ""

        for command in commands:
            plugin = self.find_plugin(command[0])
            if not plugin:
                break

            try:
                stdin = io.StringIO(pipe_buffer)
                stdout = io.StringIO()
                msg["args"] = command
                msg["message"] = " ".join(command)
                plugin.on_command(msg, stdin, stdout, reply)
                pipe_buffer = stdout.getvalue()
            except StopCommand as e:
                self.send(msg["reply_to"], str(e))
                break
            except NotImplementedError:
                break
            except Exception as e:
                traceback.print_exc()
                self.send(msg["reply_to"], repr(e))
                break
        else:
            self.send(msg["reply_to"], pipe_buffer.strip())

    def on_message(self, msg):
        self.call_plugins_on_message(msg)

        m = msg["message"].strip()
        if m.startswith(self.name) or m.startswith("!"):
            if m.startswith("!"):
                m = m[1:].strip()
            else:
                m = m[len(self.name)+1:].strip()

            msg["message"] = m

            self.call_plugins_on_respond(msg)

            target = self.call_plugins_on_command
            threading.Thread(target=target, args=(msg,)).start()

    # actions
    def join(self, channel):
        self.backend.join(channel)

    def send(self, target, message):
        self.backend.send(target, str(message))

    def format(self, text, *properties):
        return self.backend.format(text, properties)
