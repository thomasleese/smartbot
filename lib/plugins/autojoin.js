module.exports = function(bot, config) {
  config.forEach(function(channel) {
    bot.join(channel);
  });

  bot.help("autojoin", function(msg, reply) {
    reply("Automatically joins channels when the bot connects.");
  });
};
