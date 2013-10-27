var crypto = require("crypto");
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
                bot.reply(from, to, title);
              } else {
                bot.reply(from, to, "[" + i + "]: " + title);
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
                bot.reply(from, to, "[" + i + "]: " + item.link);
              });

              if (res.items.length === 0) {
                bot.reply(from, to, "No google results!")
              }
            }
          });
        }
      });
    });
  },

  encoding: function(bot, config) {
    bot.on("message", function(from, to, text) {
      var query = text.match(/base64 encode( me)? (.*)/i);
      if (query && query.length > 2) {
        bot.reply(from, to, new Buffer(query[2]).toString("base64"));
      }

      var query = text.match(/base64 decode( me)? (.*)/i);
      if (query && query.length > 2) {
        bot.reply(from, to, new Buffer(query[2], "base64").toString("utf8"));
      }
    });
  },

  hashing: function(bot, config) {
    var hexDigest = function(str, algo) {
      return crypto.createHash(algo).update(str, "utf8").digest("hex");
    }

    bot.on("message", function(from, to, text) {
      var query = text.match(/md5( me)? (.*)/i);
      if (query && query.length > 2) {
        bot.reply(from, to, hexDigest(query[2], "md5"));
      }

      var query = text.match(/sha( me)? (.*)/i);
      if (query && query.length > 2) {
        bot.reply(from, to, hexDigest(query[2], "sha"));
      }

      var query = text.match(/sha1( me)? (.*)/i);
      if (query && query.length > 2) {
        bot.reply(from, to, hexDigest(query[2], "sha1"));
      }

      var query = text.match(/sha256( me)? (.*)/i);
      if (query && query.length > 2) {
        bot.reply(from, to, hexDigest(query[2], "sha256"));
      }

      var query = text.match(/sha512( me)? (.*)/i);
      if (query && query.length > 2) {
        bot.reply(from, to, hexDigest(query[2], "sha512"));
      }

      var query = text.match(/rmd160( me)? (.*)/i);
      if (query && query.length > 2) {
        bot.reply(from, to, hexDigest(query[2], "rmd160"));
      }
    });
  }

};
