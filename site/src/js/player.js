// Player: boots the gam4988 web core (vendor/gam4988) with the firmware and a
// game from games.json, runs it at a fixed 60 Hz, and maps keyboard and touch
// input to dictionary keys. In-game saves live in the core's Flash save area,
// which is mirrored to IndexedDB whenever the game writes it.
(function () {
  'use strict';

  const KEYS = {
    ENTER: 0x2f, EXIT: 0x2e, UP: 0x35, DOWN: 0x38, LEFT: 0x37, RIGHT: 0x39,
    PGUP: 0x3a, PGDN: 0x3b, HELP: 0x29, SEARCH: 0x2a, DEL: 0x2d, SPACE: 0x36,
    SHIFT: 0x28, INPUT: 0x20
  };
  const KEYBOARD = {
    ArrowUp: 'UP', ArrowDown: 'DOWN', ArrowLeft: 'LEFT', ArrowRight: 'RIGHT',
    Enter: 'ENTER', z: 'ENTER', Z: 'ENTER', Escape: 'EXIT', x: 'EXIT', X: 'EXIT', Backspace: 'EXIT',
    PageUp: 'PGUP', PageDown: 'PGDN'
  };
  const LCD_COLOURS = { classic: [120, 140, 104], pale: [196, 204, 178], blue: [150, 180, 205] };
  const GHOSTING = 4;
  const STEP_MS = 1000 / 60;
  const REPEAT_DELAY = 300, REPEAT_EVERY = 100;
  const W = 159, H = 96;

  const $ = function (id) { return document.getElementById(id); };
  const canvas = $('screen');
  const ctx = canvas.getContext('2d');
  const image = ctx.createImageData(W, H);

  let M = null;              // emscripten module
  let rom = null;            // game bytes
  let game = null, ver = null;
  let running = false, halted = false;
  let saveKey = '', stateKey = '';
  let persistedRev = 0, seenRev = 0;

  /* ---------- UI helpers ---------- */

  let toastTimer = 0;
  function toast(msg) {
    const t = $('toast');
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.classList.remove('show'); }, 2200);
  }

  function overlay(text, progress, button) {
    $('overlay').hidden = text == null;
    $('overlay-text').textContent = text || '';
    $('overlay-bar').hidden = progress == null;
    if (progress != null) $('overlay-fill').style.width = Math.round(progress * 100) + '%';
    $('overlay-btn').hidden = !button;
    if (button) $('overlay-btn').textContent = button;
  }

  function fail(msg) {
    running = false;
    overlay(msg, null, 'Reload');
    $('overlay-btn').onclick = function () { location.reload(); };
  }

  function pref(name, fallback) {
    try { const v = localStorage.getItem('pref.' + name); return v == null ? fallback : v; } catch (e) { return fallback; }
  }
  function setPref(name, v) { try { localStorage.setItem('pref.' + name, v); } catch (e) { /* ignore */ } }

  /* ---------- screen size: whole device pixels per LCD pixel ---------- */

  function fit() {
    const dpr = window.devicePixelRatio || 1;
    const landscape = matchMedia('(orientation: landscape) and (max-height: 540px)').matches;
    const bezel = landscape ? 20 : 28;
    let maxW = Math.min(document.documentElement.clientWidth - 32, 159 * 5) - bezel;
    let maxH = window.innerHeight - bezel - (landscape ? 70 : 360);
    if (landscape) maxW = document.documentElement.clientWidth - 2 * 190 - bezel;
    maxH = Math.max(maxH, 96 * 1.5);
    const scale = Math.max(1, Math.floor(Math.min(maxW / W, maxH / H) * dpr));
    canvas.style.width = (W * scale / dpr) + 'px';
    canvas.style.height = (H * scale / dpr) + 'px';
  }
  window.addEventListener('resize', fit);

  /* ---------- core ---------- */

  function withBytes(bytes, fn) {
    const ptr = M._malloc(bytes.length);
    M.HEAPU8.set(bytes, ptr);
    try { return fn(ptr, bytes.length); } finally { M._free(ptr); }
  }

  function readBytes(size, fill) {
    const ptr = M._malloc(size);
    try { fill(ptr); return M.HEAPU8.slice(ptr, ptr + size); } finally { M._free(ptr); }
  }

  function draw() {
    const p = M._web_get_framebuffer_rgba();
    image.data.set(M.HEAPU8.subarray(p, p + W * H * 4));
    ctx.putImageData(image, 0, 0);
  }

  function applyScreenPrefs() {
    const c = LCD_COLOURS[pref('lcd', 'classic')] || LCD_COLOURS.classic;
    M._web_set_lcd_bg(c[0], c[1], c[2]);
    document.documentElement.style.setProperty('--lcd', 'rgb(' + c.join(',') + ')');
    M._web_set_lcd_ghosting(pref('ghost', '0') === '1' ? GHOSTING : 0);
    draw();
  }

  function flashBytes() {
    return readBytes(M._web_save_ram_size(), function (p) { M._web_save_ram(p); });
  }

  function persistFlash() {
    if (!M || halted) return Promise.resolve();
    const rev = M._web_save_ram_revision() >>> 0;
    if (rev === persistedRev) return Promise.resolve();
    persistedRev = rev;
    return SaveStore.set(saveKey, { data: flashBytes(), version: ver.version, at: Date.now() })
      .then(function (ok) { toast(ok ? 'Game saved in this browser' : 'Saved for this session only'); });
  }

  // The game writes Flash in bursts; persist once the revision stops moving.
  setInterval(function () {
    if (!M || halted) return;
    const rev = M._web_save_ram_revision() >>> 0;
    if (rev !== persistedRev && rev === seenRev) persistFlash();
    seenRev = rev;
  }, 700);

  function bootGame(flash) {
    if (!withBytes(rom, function (p, n) { return M._web_load_game(p, n); })) throw new Error('The game file was rejected.');
    if (flash && flash.length === M._web_save_ram_size()) {
      withBytes(flash, function (p, n) { M._web_load_save_ram(p, n); });
    }
    persistedRev = seenRev = M._web_save_ram_revision() >>> 0;
  }

  /* ---------- main loop ---------- */

  let last = 0, acc = 0, rtcLast = 0;
  function frame(ts) {
    if (!running) return;
    if (!last) { last = ts; rtcLast = rtcLast || ts; }
    acc += Math.min(Math.max(ts - last, 0), 250);
    last = ts;
    let steps = 0, changed = false;
    try {
      while (acc >= STEP_MS && steps < 6) {
        acc -= STEP_MS;
        steps += 1;
        if (M._web_run_frame()) changed = true;
      }
      if (steps === 6) acc = 0;
      const secs = Math.floor((ts - rtcLast) / 1000);
      if (secs > 0) { M._web_tick_rtc(Math.min(secs, 86400)); rtcLast += secs * 1000; }
    } catch (e) {
      return powerOff(e);
    }
    if (changed) draw();
    requestAnimationFrame(frame);
  }

  function start() {
    if (running || halted) return;
    running = true;
    last = 0;
    requestAnimationFrame(frame);
  }

  function powerOff(e) {
    running = false;
    halted = true;
    const clean = e && e.name === 'ExitStatus';
    overlay(clean ? 'The dictionary switched itself off.' : 'The emulator stopped: ' + (e && e.message || e), null, 'Turn it back on');
    $('overlay-btn').onclick = function () { location.reload(); };
  }

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { persistFlash(); running = false; } else if (M && !halted) start();
  });
  window.addEventListener('pagehide', function () { persistFlash(); });

  /* ---------- input ---------- */

  function press(name) {
    if (M && running) M._web_keydown(KEYS[name]);
  }

  function menuOpen() { return $('menu').open; }

  document.addEventListener('keydown', function (e) {
    if (menuOpen() || e.ctrlKey || e.metaKey || e.altKey) return;
    const name = KEYBOARD[e.key];
    if (!name) return;
    e.preventDefault();
    press(name);
  });

  function repeater() {
    let delay = 0, every = 0;
    return {
      start: function (fn) {
        this.stop();
        fn();
        delay = setTimeout(function () { every = setInterval(fn, REPEAT_EVERY); }, REPEAT_DELAY);
      },
      stop: function () { clearTimeout(delay); clearInterval(every); }
    };
  }

  // D-pad: one touch area, direction from the angle, slide to change direction.
  (function () {
    const pad = $('dpad');
    const rep = repeater();
    let dir = null, pointer = null;
    function dirAt(e) {
      const r = pad.getBoundingClientRect();
      const x = e.clientX - (r.left + r.width / 2), y = e.clientY - (r.top + r.height / 2);
      if (Math.hypot(x, y) < r.width * 0.12) return dir;
      return Math.abs(x) > Math.abs(y) ? (x > 0 ? 'RIGHT' : 'LEFT') : (y > 0 ? 'DOWN' : 'UP');
    }
    function set(d) {
      if (d === dir) return;
      dir = d;
      pad.dataset.dir = d ? d.toLowerCase() : '';
      if (d) rep.start(function () { press(d); }); else rep.stop();
    }
    pad.addEventListener('pointerdown', function (e) {
      e.preventDefault();
      pointer = e.pointerId;
      pad.setPointerCapture(e.pointerId);
      if (navigator.vibrate) navigator.vibrate(8);
      set(dirAt(e));
    });
    pad.addEventListener('pointermove', function (e) { if (e.pointerId === pointer) set(dirAt(e)); });
    ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(function (t) {
      pad.addEventListener(t, function (e) { if (e.pointerId === pointer) { pointer = null; set(null); } });
    });
  })();

  document.querySelectorAll('button.key[data-key]').forEach(function (b) {
    const rep = repeater();
    const name = b.dataset.key;
    b.addEventListener('pointerdown', function (e) {
      e.preventDefault();
      b.setPointerCapture(e.pointerId);
      b.classList.add('pressed');
      if (navigator.vibrate) navigator.vibrate(8);
      if ('repeat' in b.dataset) rep.start(function () { press(name); }); else press(name);
    });
    ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(function (t) {
      b.addEventListener(t, function () { b.classList.remove('pressed'); rep.stop(); });
    });
    b.addEventListener('click', function (e) { e.preventDefault(); });
  });
  document.querySelectorAll('.controls, .more-keys').forEach(function (el) {
    el.addEventListener('contextmenu', function (e) { e.preventDefault(); });
  });

  /* ---------- menu ---------- */

  $('menu-btn').addEventListener('click', function () {
    if (M && !halted) { persistFlash(); running = false; }
    $('menu').showModal();
  });
  $('menu').addEventListener('close', function () { if (M && !halted) start(); });

  $('state-save').addEventListener('click', function () {
    if (!M || halted) return;
    const bytes = readBytes(M._web_save_size(), function (p) { M._web_save(p); });
    SaveStore.set(stateKey, { data: bytes, version: ver.version, at: Date.now() }).then(function (ok) {
      toast(ok ? 'State saved' : 'State saved for this session only');
    });
    $('menu').close();
  });

  $('state-load').addEventListener('click', function () {
    if (!M || halted) return;
    SaveStore.get(stateKey).then(function (s) {
      if (!s || !s.data) { toast('No saved state yet'); return; }
      if (s.version !== ver.version) { toast('That state is from another version of the game'); return; }
      const ok = withBytes(s.data, function (p, n) { return M._web_load(p, n); });
      draw();
      toast(ok ? 'State loaded' : 'Could not load that state');
    });
    $('menu').close();
  });

  $('save-export').addEventListener('click', function () {
    if (!M || halted) return;
    const url = URL.createObjectURL(new Blob([flashBytes()], { type: 'application/octet-stream' }));
    const a = document.createElement('a');
    a.href = url;
    a.download = game.id + '-' + ver.lang + '.sav';
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 5000);
  });

  $('save-import').addEventListener('click', function () { $('save-file').click(); });
  $('save-file').addEventListener('change', function () {
    const f = this.files[0];
    this.value = '';
    if (!f || !M || halted) return;
    f.arrayBuffer().then(function (buf) {
      const data = new Uint8Array(buf);
      if (data.length !== M._web_save_ram_size()) { toast('That is not a save file for this player'); return; }
      bootGame(data);
      persistedRev = -1;
      return persistFlash().then(function () { $('menu').close(); toast('Save imported, game restarted'); });
    });
  });

  $('restart').addEventListener('click', function () {
    if (!M) return;
    if (halted) { location.reload(); return; }
    persistFlash().then(function () {
      return SaveStore.get(saveKey);
    }).then(function (s) {
      bootGame(s && s.data);
      $('menu').close();
    });
  });

  $('lcd-colour').value = pref('lcd', 'classic');
  $('lcd-colour').addEventListener('change', function () { setPref('lcd', this.value); if (M) applyScreenPrefs(); });
  $('lcd-ghost').checked = pref('ghost', '0') === '1';
  $('lcd-ghost').addEventListener('change', function () { setPref('ghost', this.checked ? '1' : '0'); if (M) applyScreenPrefs(); });
  $('show-more').checked = pref('more', '0') === '1';
  $('more-keys').hidden = !$('show-more').checked;
  $('show-more').addEventListener('change', function () {
    setPref('more', this.checked ? '1' : '0');
    $('more-keys').hidden = !this.checked;
  });

  /* ---------- loading ---------- */

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      const s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = function () { reject(new Error('Could not load ' + src)); };
      document.head.appendChild(s);
    });
  }

  // fetch with a shared progress bar over all downloads
  const progress = { got: {}, total: {} };
  function report() {
    let got = 0, total = 0;
    for (const k in progress.total) { got += progress.got[k] || 0; total += progress.total[k]; }
    if (total) overlay('Loading…', got / total);
  }
  function fetchBytes(url, expected) {
    progress.total[url] = expected || 1;
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error('Download failed: ' + url + ' (' + r.status + ')');
      if (!r.body || !r.body.getReader) return r.arrayBuffer().then(function (b) { return new Uint8Array(b); });
      const reader = r.body.getReader();
      const parts = [];
      let n = 0;
      function pump() {
        return reader.read().then(function (res) {
          if (res.done) {
            const out = new Uint8Array(n);
            let o = 0;
            for (const p of parts) { out.set(p, o); o += p.length; }
            return out;
          }
          parts.push(res.value);
          n += res.value.length;
          progress.got[url] = Math.min(n, progress.total[url]);
          report();
          return pump();
        });
      }
      return pump();
    });
  }

  function boot() {
    const q = new URLSearchParams(location.search);
    fit();
    overlay('Loading…', 0);
    fetch('games.json').then(function (r) {
      if (!r.ok) throw new Error('Could not load the game list.');
      return r.json();
    }).then(function (cat) {
      game = cat.games.find(function (g) { return g.id === q.get('g'); });
      if (!game) throw new Error('Unknown game.');
      ver = game.versions.find(function (v) { return v.lang === (q.get('v') || 'en'); }) || game.versions[0];
      document.title = game.title + (ver.lang === 'en' ? '' : ' (' + ver.label + ')') + ' · BBK Games in English';
      $('game-title').textContent = game.title;
      $('game-sub').textContent = ver.label + ' · ' + ver.version;
      $('menu-title').textContent = game.title;
      $('menu-version').textContent = game.title_zh + ' · ' + ver.label + ' ' + ver.version + ' · ' + ver.status;
      saveKey = 'flash/' + game.id + '/' + ver.lang;
      stateKey = 'state/' + game.id + '/' + ver.lang;
      return Promise.all([
        loadScript('vendor/gam4988/gam4988.js').then(function () {
          return window.Gam4988Module({ locateFile: function (p) { return 'vendor/gam4988/' + p; } });
        }),
        fetchBytes(cat.bios, 4 << 20),
        fetchBytes(ver.url, ver.size),
        SaveStore.get(saveKey)
      ]);
    }).then(function (r) {
      M = r[0];
      rom = r[2];
      if (withBytes(r[1], function (p, n) { return M._web_init(p, n); }) !== 0) throw new Error('The firmware did not start.');
      bootGame(r[3] && r[3].data);
      applyScreenPrefs();
      overlay(null);
      start();
      if (r[3] && r[3].data) toast('Loaded your saves from this browser');
    }).catch(function (e) {
      fail(e && e.message ? e.message : String(e));
    });
  }

  boot();
})();
