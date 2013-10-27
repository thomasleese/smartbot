var Browser = require("zombie");

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
    bot.on("message", function(from, to, text, message) {
      var sendTo = to;
      if (to === bot.nick) {
        sendTo = from;
      }

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
                bot.say(sendTo, title);
              } else {
                bot.say(sendTo, "[" + i + "]: " + title);
              }
            }

            browser.close();
          });
        });
      }
    });
  }

};
