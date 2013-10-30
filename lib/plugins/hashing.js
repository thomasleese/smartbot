var crypto = require("crypto");

module.exports = function(bot, config) {
  bot.respond(/(md5|sha|sha1|sha256|sha512) (.*)$/i, function(msg, reply) {
    var hash = crypto.createHash(msg.match[1]);
    hash.update(msg.match[2], "utf8");
    reply(hash.digest("hex"));
  });

  bot.help("hashing", function(msg, reply) {
    reply("Syntax: md5|sha|sha1|sha256|sha512 value");
  });
};
