var Sandbox = require("sandbox");

module.exports = function(bot, config) {
  bot.respond(/(run|sandbox|js) (.*)$/i, function(msg, reply) {
    var s = new Sandbox();
    s.run(msg.match[2], function(output) {
      output.console.forEach(function(c) {
        reply(c.replace(/(\r\n|\n|\r)/gm, ""));
      })

      reply(output.result.replace(/(\r\n|\n|\r)/gm, ""));
    });
  });
};
