var wolfram = require("wolfram-alpha");

var wolframString = function(input) {
  if (input.text.trim().length <= 0 || input.text.trim().length >= 400) {
    return input.image;
  }

  var s = input.text;
  // first we convert any of those wierd unicode chars
  var regex = /\\:([A-Za-z0-9]+)/g;
  s = s.replace(regex, function(_, arg) {
    return String.fromCharCode(parseInt(arg, 16));
  });

  // then turn it into a table... if it is one
  if (s.indexOf("|") === -1) {
    return s.trim();
  } else {
    var rows = s.split(/\r\n|\n|\r/);
    var maximumColumnWidths = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ];
    rows = rows.map(function(row) {
      return row.split(/\|/).map(function(col, colIndex) {
        var c = col.trim();
        if (c.length > maximumColumnWidths[colIndex]) {
          maximumColumnWidths[colIndex] = c.length;
        }
        return c;
      });
    });

    var result = "";
    rows.forEach(function(row) {
      result += "|";

      row.forEach(function(col, colIndex) {
        result += " " + col;
        var count = maximumColumnWidths[colIndex] + 2 - col.length;
        result += (new Array(count)).join(" ");
        result += "|";
      });

      result += "\n";
    });

    return result.trim();
  }
};

module.exports = function(bot, config) {
  var w = wolfram.createClient(config);

  var wolframRegex = /^(\?|q|question|wfa|calc|calculate) (.*)$/i;
  bot.on("message", function(from, to, text) {
    var query = text.match(wolframRegex);
    if (query && query.length > 2) {
      w.query(query[2], function(err, result) {
        if (result && result.length > 1) {
          var smallResult = wolframString(result[0].subpods[0]) + " => " + wolframString(result[1].subpods[0]);
          if (smallResult.length <= 100 && smallResult.indexOf("\n") === -1) {
            bot.reply(from, to, smallResult);
          } else {
            result.forEach(function(pod, i) {
              if (i >= 2) {
                return;
              }

              bot.reply(from, to, "# " + pod.title);
              pod.subpods.forEach(function(subpod) {
                if (subpod.title) {
                  bot.reply(from, to, "## " + subpod.title);
                }

                bot.reply(from, to, wolframString(subpod));
              });
            });

            bot.reply(from, to, "http://www.wolframalpha.com/input/?i=" + encodeURIComponent(query[2]));
          }
        } else {
          bot.reply(from, to, "Hmm... not sure");
        }
      });
    }
  });
};
