module.exports = function(bot, config) {

  bot.hear(/.*/, function(msg, reply) {
    bot.storage.put("seen." + msg.from, {
      action: "spoke",
      date: new Date()
    });
  });

  bot.respond(/(?:last)?seen (.*)$/, function(msg, reply) {
    var info = bot.storage.get("seen." + msg.match[1]);
    if (info) {
      reply(msg.match[1] + " " + info.action + " on " + info.date);
    } else {
      reply("I don't know anything about " + msg.match[1] + ".");
    }
  });

};
