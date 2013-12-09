module.exports = function(bot, config) {

  bot.respond(/(throw|flip|toss)( a)? coin/i, function(msg, reply) {
    var i = Math.floor(Math.random() * 2);
    if (i == 0) {
      reply("heads");
    } else {
      reply("tails");
    }
  });

  bot.help("coin", function(msg, reply) {
    reply("Throws coins");
    reply("Syntax: throw|flip|toss [a] coin");
  });

};
