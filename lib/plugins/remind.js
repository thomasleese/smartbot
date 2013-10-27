var moment = require("moment");
var sugar = require("sugar");

var REGEX = /remind me (to|about) (.*) (in|at) (.*)$/i;

module.exports = function(bot, config) {
  bot.respond(REGEX, function(msg, reply) {
    var action = msg.match[2];
    var time = msg.match[4];

    var date = Date.future(time);
    if (!date.isValid()) {
      date = Date.future("in " + time);
    }

    if (date.isValid()) {
      reply("Sure thing, " + msg.from + " (" + date.long() + ")!");
      setTimeout(function() {
        reply(msg.from + ": you reminded me to tell you " + msg.match[1] + " " + action);
      }, date - Date.create());
    } else {
      reply("I don't understand that date.");
    }
  });
};
