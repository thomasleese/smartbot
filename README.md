# Smart Bot

_A supposedly smart IRC bot._

## Configuration

The configuration file is a very simple and self-explanatory YAML based file.
Before you run the bot you must create a configuration file similar to this.

    bot:
        name: SmartBot

    backend:
        name: irc
        hostname: my.irc.server

    storage:
        name: yaml

    plugins:
        - name: autojoin
          channels: [ "#robots" ]

## Running

    $ ./bin/smartbot

## Plugins

To see the list of plugins, look in the `plugins` directory.
