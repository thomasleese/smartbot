var irc = require("irc");

var Bot = module.exports = function(server, port, nick, username, realname) {
  this.nick = nick || "SmartBot";

  this.irc = new irc.Client(server, this.nick, {
    port: port || 6667,
    userName: username || "SmartBot",
    realName: realname || "The One and Only Smart Bot",
    debug: true
  });

  this.irc.on("error", function(msg) {
    console.log(msg);
  });
};

Bot.prototype.on = function(event, callback) {
  this.irc.on(event, callback);
};

Bot.prototype.join = function(channel) {
  this.irc.join(channel);
};

Bot.prototype.say = function(target, msg) {
  this.irc.say(target, msg);
};

Bot.prototype.reply = function(from, to, msg) {
  if (to === this.nick) {
    this.say(from, msg);
  } else {
    this.say(to, msg);
  }
};
