module.exports = function(bot, config) {
  bot.respond(/your face is (.*)$/i, function(msg, reply) {
    reply("Oh yeah... well, your face is...");
    reply("!face " + msg.from);
  });  
};
