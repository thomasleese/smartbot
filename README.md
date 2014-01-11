# Smart Bot

_A supposedly smart IRC bot._

## Configuration

The configuration file is a very simple and self-explanatory YAML based file.
Before you run the bot you must create a configuration file similar to this.

    backend:
        name: irc
        hostname: my.irc.server
        port: 6667
        nick: SmartBot

    storage:
        name: yaml

    plugins:
        - name: autojoin
          channels: [ "#robots" ]

## Plugins

### autojoin

Joins channels when the bot connects.

    channels: [ "#achannel", "#anotherone" ]

### nicebot

Messages the password to the nick when you join the channel.

    channel: "#achannel"
    user: NiceBot
    password: apassword
