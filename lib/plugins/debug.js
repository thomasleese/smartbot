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
    reply("Syntax: ping | echo <msg> | time");
  });

  if (config) {
    bot.join(config);
    var oldConsoleLog = console.log;
    console.log = function() {
      var args = Array.prototype.slice.call(arguments);
      args.map(function(elem) {
        if (elem === null) {
          return "null";
        } else if (elem === undefined) {
          return "undefined";
        } else {
          return elem.toString();
        }
      });

      var s = args.join(" ");
      oldConsoleLog(s);
      bot.say(config, s);
    };
  }
};
