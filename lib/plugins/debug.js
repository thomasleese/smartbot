module.exports = function(bot, config) {
  bot.respond(/ping$/i, function(msg, reply) {
    reply("PONG");
  });

  bot.respond(/echo (.*)$/i, function(msg, reply) {
    reply(msg.match[1]);
  });

  bot.respond(/time$/i, function(msg, reply) {
    reply(new Date());
  });

  bot.help("debug", function(msg, reply) {
    reply("Syntax: ping|echo msg|time");
  });
};
