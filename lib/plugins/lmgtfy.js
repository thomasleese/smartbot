module.exports = function(bot, config) {
  
  bot.hear(/lmgtfy (.*)$/i, function(msg, reply) {
    var link = "http://lmgtfy.com/?q=" + encodeURIComponent(msg.match[1]);
    reply(link);
  });

  bot.help("lmgtfy", function(msg, reply) {
    reply("Syntax: lmgtfy <something>");
  });

};
