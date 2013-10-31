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

  this.irc.setMaxListeners(256);
  this.helpTopics = [  ];

  this.respond(/help(?: (.*))?$/i, function(msg, reply) {
    if (msg.match[1]) {
      var name = msg.match[1];
      if (this.helpTopics.indexOf(name) !== -1) {
        this.irc.emit("help#" + name, reply);
      } else {
        reply("No such help topic!");
      }
    } else {
      reply("Help about " + this.helpTopics.sort().join(", ") + "?");
    }
  }.bind(this));
};

Bot.prototype.addPlugin = function(name, config) {
  console.log("adding plugin:", name);
  var plugin = require("./plugins/" + name);
  this.irc.on("registered", function() {
    plugin(this, config);
  }.bind(this));
};

Bot.prototype.getChannel = function(name) {
  return this.irc.chans[name];
};

// actions
Bot.prototype.join = function(channel) {
  this.irc.join(channel);
};

Bot.prototype.say = function(target, msg) {
  this.irc.say(target, msg);
};

// event listeners
Bot.prototype.hear = function(regex, callback) {
  this.irc.on("message", function(from, to, text) {
    var match = text.match(regex);
    if (match) {
      var replyTo = to;
      if (to == this.nick) {
        replyTo = from;
      }

      callback({
        match: match,
        from: from,
        to: to,
        text: text,
        replyTo: replyTo,
      }, this.say.bind(this, replyTo));
    }
  }.bind(this));
};

Bot.prototype.respond = function(regex, callback) {
  var re = regex.toString().split("/");
  re.shift();
  var modifiers = re.pop();
  var pattern = re.join("/");

  var newRegex = new RegExp("^(?:" + this.nick + "[:,]?|!)\\s*(?:" + pattern + ")", modifiers);
  this.hear(newRegex, callback);
};

Bot.prototype.entered = function(callback) {
  this.irc.on("join", function(channel, nick) {
    callback({
      channel: channel,
      room: channel,
      nick: nick,
      person: nick,
      isMe: nick === this.nick
    })
  }.bind(this));
};

Bot.prototype.help = function(name, callback) {
  console.log("adding help topic:", name);
  this.helpTopics.push(name);
  this.irc.on("help#" + name, function(reply) {
    callback({ }, reply);
  });
};
