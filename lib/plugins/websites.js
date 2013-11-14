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
        cache[url] = title.replace(/(\r\n|\n|\r)/gm, "");
        callback(title);
      }
    }
  });
};

module.exports = function(bot, config) {
  bot.hear(/(https?:\/\/[^\s]+)/g, function(msg, reply) {
    var urls = msg.match;
    urls.forEach(function(url, i) {
      getTitleForURL(url, function(title) {
        if (urls.length === 1) {
          reply(title);
        } else {
          reply("[" + i + "]: " + title);
        }
      });
    });
  });

  bot.help("websites", function(msg, reply) {
    reply("Echos the titles of websites for any URLs.");
  });
};
