var Browser = require("zombie");

var BROWSER_CONFIG = {
  runScripts: false,
  loadCSS: false,
  maxWait: 5,
  userAgent: "Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0"
};

module.exports = function(bot, config) {
  bot.respond(/(developer('s|s)? |programmer('s|s)? )?excuse( me)?/i, function(msg, reply) {
    var browser = new Browser(BROWSER_CONFIG);
    browser.visit("http://developerexcuses.com/", function() {
      var thing = browser.text(".wrapper a");
      if (thing && thing.length > 0) {
        reply(thing);
      } else {
        reply("You have on excuse!");
      }
      browser.close();
    });
  });

  bot.help("excuses", function(msg, reply) {
    reply("Syntax: excuse me");
  });
};
