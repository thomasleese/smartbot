var cheerio = require("cheerio");
var request = require("request");

module.exports = function(bot, config) {
  bot.respond(/(developer('s|s)? |programmer('s|s)? )?excuse( me)?/i, function(msg, reply) {
    request("http://developerexcuses.com/", function(err, res, body) {
      if (res.statusCode === 200) {
        var $ = cheerio.load(body);
        var thing = $(".wrapper a").text();
        if (thing && thing.length > 0) {
          reply(thing);
        } else {
          reply("You have no excuse!");
        }
      }
    });
  });

  bot.help("excuses", function(msg, reply) {
    reply("Syntax: excuse me");
  });
};
