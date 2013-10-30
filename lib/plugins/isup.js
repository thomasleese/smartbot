var request = require("request");

module.exports = function(bot, config) {
  bot.respond(/is (.*?) (up|down)(\?)?/i, function(msg, reply) {
    var options = {
      url: "http://isitup.org/" + encodeURIComponent(msg.match[1]) + ".json",
      headers: {
        "User-Agent": "SmartBot"
      },
      json: true
    };

    request(options, function(err, res, body) {
      if (body.status_code === 1) {
        reply(body.domain + " looks up for me.");
      } else if (body.status_code === 2) {
        reply(body.domain + " looks down for me.");
      } else {
        reply("I don't know what you're talking about.");
      }
    });
  });
};
