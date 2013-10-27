var irc = require("irc");

var Bot = module.exports = function(server, port, nick, username, realname) {
  this.nick = nick || "SmartBot";

  this.irc = new irc.Client(server, this.nick, {
    port: port || 6667,
    userName: username || "SmartBot",
    realName: realname || "The One and Only Smart Bot",
    floodProtection: true,
    debug: true,
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

Bot.prototype.getReplyTo = function(from, to) {
  if (to === this.nick) {
    return from;
  }

  return to;
};

Bot.prototype.reply = function(from, to, msg) {
  this.say(this.getReplyTo(from, to), msg);
};

Bot.prototype.hear = function(regex, callback) {
  this.irc.on("message", function(from, to, text) {
    var match = text.match(regex);
    if (match) {
      var replyTo = this.getReplyTo(from, to);
      callback({
        match: match,
        from: from,
        to: to,
        text: text,
        replyTo: replyTo
      }, this.say.bind(this, replyTo));
    }
  }.bind(this));
};

Bot.prototype.respond = function(regex, callback) {
  this.hear(regex, callback);
};
