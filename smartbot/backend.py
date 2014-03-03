import random
import socket
import threading
import time


class _Backend:
    def __init__(self):
        self.storage = None
        self.event_listeners = []

    def add_event_listener(self, name, callback):
        self.event_listeners.append((name, callback))

    def dispatch_event(self, name, *event):
        for listener in self.event_listeners:
            if listener[0] == name:
                listener[1](*event)


class IRC(_Backend):
    def __init__(self, hostname, port=6667, username=None, realname=None):
        super().__init__()
        self.hostname = hostname
        self.port = port
        self.nick = None
        self.username = username
        self.realname = realname
        self.channels = []

        self.lock = threading.Lock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def ping_thread(self):
        while True:
            time.sleep(60)
            msg = "ping-" + str(random.randint(0, 100))
            self.write("PING", msg)

    def write(self, *args):
        def convert_part(x):
            x = bytes(x, "utf-8").strip()
            if b" " in x:
                return b":" + x
            else:
                return x

        with self.lock:
            line = b" ".join([convert_part(x) for x in args])
            line += b"\r\n"
            self.socket.send(line)

    def parse_usermask(self, usermask):
        return usermask.split("!")[0]

    def parse(self, args):
        if args[0] == "PING":
            self.write("PONG", args[1])
        elif args[1] == "001":
            self.dispatch_event("ready")
        elif args[1] == "JOIN":
            nick = self.parse_usermask(args[0])
            self.channels.append(args[2])
            self.dispatch_event("join", {
                "user": nick, "channel": args[2], "is_me": nick == self.nick
            })
        elif args[1] == "KICK":
            nick = self.parse_usermask(args[3])
            if nick == self.nick:
                self.join(args[2])
        elif args[1] == "PRIVMSG":
            sender = self.parse_usermask(args[0])
            target = args[2]
            message = args[3]

            reply_to = target
            if target == self.nick:
                reply_to = sender

            self.dispatch_event("message", {
                "sender": sender, "target": target,
                "message": message, "reply_to": reply_to
            })
        else:
            print(args)

    def run(self, name):
        self.nick = name
        if not self.username:
            self.username = self.nick
        if not self.realname:
            self.realname = self.nick

        self.socket.connect((self.hostname, self.port))

        self.dispatch_event("connect")

        thread = threading.Thread(target=self.ping_thread)
        thread.daemon = True
        thread.start()

        self.write("NICK", self.nick)
        self.write("USER", self.username, "8", "*", self.realname)

        buf = b""
        while True:
            data = self.socket.recv(4096)
            if not data:
                break

            array = (buf + data).split(b"\n")
            for line in array[:-1]:
                args = line.strip().split(b" ")
                line = []
                for i, p in enumerate(args):
                    if p.startswith(b":"):
                        if i != 0:
                            line.append((b" ".join(args[i:]))[1:])
                            break
                        elif i == 0:
                            line.append(p[1:])
                    else:
                        line.append(p)

                self.parse([str(x, "utf-8", "ignore") for x in line])

            buf = array[-1]

        self.dispatch_event("disconnect")

    def join(self, channel):
        self.write("JOIN", channel)

    def send(self, target, message):
        for msg in message.splitlines():
            self.write("PRIVMSG", target, msg)
            time.sleep(1)


class CommandLine(_Backend):
    def __init__(self):
        super().__init__()

    def run(self, name):
        self.dispatch_event("connect")
        self.dispatch_event("ready")

        while True:
            line = input("> ").strip()
            self.dispatch_event("message", {
                "sender": "stdin", "target": "stdout",
                "message": line, "reply_to": "stdin"
            })

        self.dispatch_event("disconnect")

    def join(self, channel):
        print("Joining", channel)

    def send(self, target, message):
        print(target + ":", message)
