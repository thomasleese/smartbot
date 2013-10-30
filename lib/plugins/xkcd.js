var Browser = require("zombie");

var BROWSER_CONFIG = {
  runScripts: false,
  loadCSS: false,
  maxWait: 5,
  userAgent: "Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0"
};

module.exports = function(bot, config) {
  bot.hear(/xkcd\s+(\d+)/i, function(msg, reply) {
    var url = "http://xkcd.com/" + msg.match[1];
    var browser = new Browser(BROWSER_CONFIG);
    browser.visit(url, function() {
      var title = browser.text("title");
      if (title && title.length > 0) {
        reply(url + " -> " + title);
      } else {
        reply(url);
      }

      browser.close();
    });
  });

  bot.help("xkcd", function(msg, reply) {
    reply("Syntax: xkcd num");
  });
};
