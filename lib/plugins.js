var phantom = require("phantom");

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
    phantom.create("--load-images=no", function(ph) {
      bot.on("message", function(from, to, text, message) {
        var sendTo = to;
        if (to === bot.nick) {
          sendTo = from;
        }

        var urls = text.match(urlRegex);
        for (var i = 0; i < urls.length; i++) {
          (function(i, url) {
            ph.createPage(function(page) {
              page.open(url, function(status) {
                page.get("title", function(title) {
                  if (urls.length === 1) {
                    bot.say(sendTo, title);
                  } else {
                    bot.say(sendTo, "[" + i + "]: " + title);
                  }

                  page.close();
                });
              });
            });
          }(i, urls[i]));
        }
      });
    });
  }

};
