var Browser = require("zombie");
var request = require("request");
var googleapis = require("googleapis");

module.exports = {

  autojoin: function(bot, config) {
    bot.on("registered", function() {
      config.forEach(function(channel) {
        bot.join(channel);
      });
    });
  },

  nicebot: function(bot, config) {
    bot.on("join" + config.channel, function(nick, msg) {
      if (nick === bot.nick) {
        bot.say(config.nick, config.password);
      }
    });
  },

  websites: function(bot, config) {
    var urlRegex = /(https?:\/\/[^\s]+)/g;
    bot.on("message", function(from, to, text) {
      var urls = text.match(urlRegex);
      if (urls) {
        urls.forEach(function(url, i) {
          var browser = new Browser({
            runScripts: false,
            loadCSS: false,
            maxWait: 10
          });

          browser.visit(url, function() {
            var title = browser.text("title");
            if (title.length > 0) {
              if (urls.length === 1) {
                bot.reply(to, from, title);
              } else {
                bot.reply(to, from, "[" + i + "]: " + title);
              }
            }

            browser.close();
          });
        });
      }
    });
  },

  google: function(bot, config) {
    var googleRegex = /^(google|search)( me)? (.*)/i
    googleapis.discover("customsearch", "v1").execute(function(err, client) {
      bot.on("message", function(from, to, text) {
        var query = text.match(googleRegex);
        if (query && query.length >= 4) {
          var req = client.customsearch.cse.list({ q: query[3], num: 3, cx: config.cx }).withApiKey(config.key);
          req.execute(function(err, res) {
            if (res.items) {
              res.items.forEach(function(item, i) {
                bot.reply(to, from, "[" + i + "]: " + item.link);
              });

              if (res.items.length === 0) {
                bot.reply(to, from, "No google results!")
              }
            }
          });
        }
      });
    });
  }

};
