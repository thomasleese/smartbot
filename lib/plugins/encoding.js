module.exports = function(bot, config) {
  
  bot.respond(/(?:base64|b64) encode (.*)$/i, function(msg, reply) {
    reply(new Buffer(msg.match[1]).toString("base64"));
  });

  bot.respond(/(?:base64|b64) decode (.*)$/i, function(msg, reply) {
    reply(new Buffer(msg.match[1], "base64").toString("utf8"));
  });

  bot.help("encoding", function(msg, reply) {
    reply("Syntax: base64|b64 encode|decode <text>");
  });

};
