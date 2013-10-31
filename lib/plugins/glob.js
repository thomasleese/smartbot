var minimatch = require("minimatch");

var escapeRegExp = function(str) {
  return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
}

module.exports = function(bot, config) {
  bot.hear(/\{([^\}]*)\}/gi, function(msg, reply) {
    var m = msg.text;
    msg.match.forEach(function(glob) {
      var replacement = [];
      var channel = bot.getChannel(msg.to); // to will be a channel or me
      for (var nick in channel.users) {
        var g = glob.substring(1, glob.length - 1);
        if (minimatch(nick, g)) {
          replacement.push(nick);
        }
      }

      if (replacement.length === 0) {
        replacement.push("no matches");
      }

      m = m.replace(new RegExp(escapeRegExp(glob)), replacement.join(", "));
    });

    reply(m);
  });
};
