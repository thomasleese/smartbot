var cheerio = require("cheerio");
var request = require("request");

var getContentTypeForURL = function(url, callback) {
  var opts = {
    url: url,
    timeout: 10 * 1000,
    method: "HEAD"
  };

  request(opts, function(err, res, body) {
    if (!err) {
      callback(res.headers["content-type"]);
    } else {
      callback(null);
    }
  });
};

var getTitleForURL = function(url, callback) {
  console.log("Scraping:", url);
  getContentTypeForURL(url, function(contentType) {
    if (contentType && contentType.indexOf("text/html") === 0) {
      request(url, function(err, res, body) {
        if (!err) {
          var $ = cheerio.load(body);
          var title = $("title").text();
          if (title && title.length > 0) {
            title = title.replace(/[\n|\r]/g, "").trim();
            callback(title);
          }
        }
      });
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
