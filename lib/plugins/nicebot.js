module.exports = function(bot, config) {
  bot.entered(function(msg) {
    if (msg.channel === config.channel
        && (msg.isMe || msg.nick === config.nick)) {
      bot.say(config.nick, config.password);
    }
  });

  bot.help("nicebot", function(msg, reply) {
    reply("Automatically registers with NiceBot when joining a channel.");
  });
};
