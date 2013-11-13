var cheerio = require("cheerio");
var request = require("request");

var cache = [ ];

var getTitleForURL = function(url, callback) {
  console.log("Scraping:", url);
  if (cache[url]) {
    return callback(cache[url]);
  }

  var opts = {
    url: url,
    timeout: 30 * 1000
  };

  request(opts, function(err, res, body) {
    if (res.statusCode === 200) {
      var $ = cheerio.load(body);
      var title = $("title").text();
      if (title && title.length > 0) {
        cache[url] = title;
        callback(title);
      } else {
        callback(null);
      }
    } else {
      callback(null);
    }
  });
};

module.exports = function(bot, config) {
  bot.hear(/xkcd\s+(\d+)/i, function(msg, reply) {
    var url = "http://xkcd.com/" + msg.match[1];
    getTitleForURL(url, function(title) {
      if (title) {
        reply(url + " -> " + title);
      } else {
        reply(url);
      }
    });
  });

  bot.help("xkcd", function(msg, reply) {
    reply("Syntax: xkcd num");
  });
};
