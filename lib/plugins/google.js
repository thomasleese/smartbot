var googleapis = require("googleapis");

module.exports = function(bot, config) {
  googleapis.discover("customsearch", "v1").execute(function(err, client) {
    bot.respond(/(?:google|search)(?: for) (.*)$/i, function(msg, reply) {
      var query = { q: msg.match[1], num: 3, cx: config.cx };
      var req = client.customsearch.cse.list(query).withApiKey(config.key);
      req.execute(function(err, res) {
        if (res.items) {
          res.items.forEach(function(item, i) {
            reply("[" + i + "]: " + item.link);
          });

          if (res.items.length === 0) {
            reply("No google results!")
          }
        }
      });
    });
  });

  bot.help("google", function(msg, reply) {
    reply("Syntax: google|search [for] <query>");
  });
};
