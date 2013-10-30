# Smart Bot

_A supposedly smart IRC bot._

Smart Bot is a very thin wrapper around the excellent [node IRC library][0]. It
is very loosely based on Hubot in the sense that it uses a similar plugin API.

The logic of the bot is controlled using plugins.

## Configuration

The configuration file is a very simple and self-explanatory JSON based config.
Before you run the bot you must create a configuration file similar to this.

	{
		"irc": {
			"server": "my.irc.server.com",
			"port": 6667,
			"nick": "SmartBot",
			"username": "SmartBot",
			"realname": "The one and only bot"
		},

		"plugins": {
			"autojoin": [ "#channel1", "#channel2" ],
			"websites": null,
			"google": { "key": "mygooglekey", "cx": "mycxkey" },
			"encoding": null,
			"hashing": null,
			"xkcd": null,
			"wolfram": "mywolframkey",
			"remind": null
		}

	}

## Plugins

### autojoin

Joins channels when the bot connects.

	"autojoin": [ "#achannel", "#anotherone" ]

### nicebot

PRIVMSGs the password to the nick when you join the channel.

	"nicebot": { "channel": "#achannel", "nick": "NiceBot", "password": "apassword" }

### websites

Writes out the title of websites that anyone has said based on the URLs.

	"websites": null

### google

Searches google.

	"google": { "key": "google_api_key", "cx": "custom_search_cx" }

### encoding

Lots of encoding functions.

	"encoding": null

### hashing

Lots of hashing functions.

	"hashing": null

### xkcd

Some XKCD lookups.

	"xkcd": null

### wolfram

Perform Wolfram|Alpha calculations.

	"wolfram": "api_key"

### remind

"remind me to <action> in <time>"
"remind me to <action> at <time>"

	"remind": null

### rules

Every robot should know the rules.

	"rules": null

### debug

General debugging commands.

	"debug": null

[0]: https://github.com/martynsmith/node-irc
