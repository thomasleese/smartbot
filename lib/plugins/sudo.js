module.exports = function(bot, config) {
  
  bot.respond(/(?:sudo) ?(.*)/i, function(msg, reply) {
    if (msg.match[1]) {
      reply("Alright, I'll " + msg.match[1] + ".");
    } else {
      reply("Alright, I'll do whatever it is you want.");
    }
  });

};
