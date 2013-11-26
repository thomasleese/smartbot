module.exports = function(bot, config) {
  
  var regex = /(what are )?the (three |3 )?(rules|laws)/i;
  bot.respond(regex, function(msg, reply) {
    reply("1. A robot may not injure a human being or, through inaction, allow a human being to come to harm.");
    reply("2. A robot must obey any orders given to it by human beings, except where such orders would conflict with the First Law.");
    reply("3. A robot must protect its own existence as long as such protection does not conflict with the First or Second Law.");
  });

};
