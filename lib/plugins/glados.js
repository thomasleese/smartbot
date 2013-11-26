module.exports = function(bot, config) {

  bot.hear(/bring( your)? daughter( to)? work( day)?/i, function(msg, reply) {
    reply("Remember, the Aperture Science 'Bring Your Daughter to Work Day' is the perfect time to have her tested.");
  });

  bot.hear(/(vital )?organ donor/i, function(msg, reply) {
    reply("Did you know you can donate one or all of your vital organs to the Aperture Science Self-Esteem Fund for Girls? It's true!");
  });

  bot.hear(/(the )?cake is( a)? lie/i, function(msg, reply) {
    reply("The Enrichment Center is required to remind you that you will be baked, and then there will be cake.");
  });

  bot.hear(/(weighted )?companion cube/i, function(msg, reply) {
    reply("We at the Enrichment Center would like to remind you that the Weighted Companion Cube will never threaten to stab you, and in fact, cannot speak.");
  });

  bot.help("glados", function(msg, reply) {
    reply("She's listening...");
  });
  
};
