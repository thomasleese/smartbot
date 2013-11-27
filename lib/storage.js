var fs = require("fs");

var storage = {};

try {
  storage = JSON.parse(fs.readFileSync("storage.json"));
} catch (e) {
  // ok...
}

module.exports = {

  put: function(key, value) {
    storage[key] = value;
    this.commit();
  },

  get: function(key, defaultValue) {
    return storage[key] || defaultValue;
  },

  commit: function() {
    var s = JSON.stringify(storage);
    fs.writeFileSync("storage.json", s);
  }

};
