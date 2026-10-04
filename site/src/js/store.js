// Tiny IndexedDB key-value store for saves. Falls back to memory (lost on
// reload) when IndexedDB is unavailable, e.g. some private windows.
window.SaveStore = (function () {
  'use strict';
  const memory = new Map();
  let dbPromise = null;

  function db() {
    if (!dbPromise) {
      dbPromise = new Promise(function (resolve, reject) {
        const req = indexedDB.open('bbk-games-en', 1);
        req.onupgradeneeded = function () { req.result.createObjectStore('kv'); };
        req.onsuccess = function () { resolve(req.result); };
        req.onerror = function () { reject(req.error); };
      });
    }
    return dbPromise;
  }

  function run(mode, fn) {
    return db().then(function (d) {
      return new Promise(function (resolve, reject) {
        const tx = d.transaction('kv', mode);
        const req = fn(tx.objectStore('kv'));
        tx.oncomplete = function () { resolve(req.result); };
        tx.onerror = tx.onabort = function () { reject(tx.error); };
      });
    });
  }

  return {
    persistent: true,
    get: function (key) {
      return run('readonly', function (s) { return s.get(key); }).catch(function () {
        this.persistent = false;
        return memory.get(key);
      }.bind(this));
    },
    set: function (key, value) {
      memory.set(key, value);
      return run('readwrite', function (s) { return s.put(value, key); })
        .then(function () { return true; })
        .catch(function () { this.persistent = false; return false; }.bind(this));
    }
  };
})();
