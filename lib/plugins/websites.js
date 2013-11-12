var Browser = require("zombie");

var BROWSER_CONFIG = {
  runScripts: false,
  loadCSS: false,
  maxWait: 20,
  userAgent: "Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0"
};

module.exports = function(bot, config) {
  bot.hear(/(https?:\/\/[^\s]+)/g, function(msg, reply) {
    var urls = msg.match;
    urls.forEach(function(url, i) {
      var browser = new Browser(BROWSER_CONFIG);
      browser.visit(url, function() {
        var title = browser.text("title");
        if (title && title.length > 0) {
          if (urls.length === 1) {
            reply(title);
          } else {
            reply("[" + i + "]: " + title);
          }
        }

        browser.close();
      });
    });
  });

  bot.help("websites", function(msg, reply) {
    reply("Echos the titles of websites for any URLs.");
  });
};
