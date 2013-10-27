# Smart Bot

A supposedly smart IRC bot.

## Plugins

### autojoin

Joins channels when the bot connects.

	"autojoin": [ "#achannel", "#anotherone" ]

### nicebot

PRIVMSGes the password to the nick when you join the channel.

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
