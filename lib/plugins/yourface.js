module.exports = function(bot, config) {

  bot.respond(/your face is (.*)$/i, function(msg, reply) {
    reply("Oh yeah... well, your face is...");
    reply("!face " + msg.from);
  });

  bot.help("yourface", function(msg, reply) {
    reply("That's right!");
  });

};
