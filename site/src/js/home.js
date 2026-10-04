// Library cards from games.json (written by tools/site/build.py).
(function () {
  'use strict';
  const box = document.getElementById('games');

  function el(tag, attrs, children) {
    const e = document.createElement(tag);
    for (const k in attrs || {}) {
      if (k === 'text') e.textContent = attrs[k];
      else e.setAttribute(k, attrs[k]);
    }
    for (const c of children || []) if (c) e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    return e;
  }

  function playUrl(game, v) {
    return 'play.html?g=' + encodeURIComponent(game.id) + '&v=' + encodeURIComponent(v.lang);
  }

  function card(game) {
    const en = game.versions.find(function (v) { return v.lang === 'en'; }) || game.versions[0];
    const others = game.versions.filter(function (v) { return v !== en; });
    const shot = en.shot ? el('img', { class: 'shot', src: en.shot, alt: game.title + ' title screen', width: 318, height: 192 }) : null;
    const buttons = [el('a', { class: 'button primary', href: playUrl(game, en), text: 'Play in ' + en.label })];
    for (const v of others) buttons.push(el('a', { class: 'button', href: playUrl(game, v), text: v.label }));
    if (en.patch) buttons.push(el('a', { class: 'small-link', href: en.patch, download: '', text: 'Patch (.bps)' }));
    return el('article', { class: 'card' }, [
      shot,
      el('div', {}, [
        el('h3', {}, [game.title, el('span', { class: 'badge', text: en.status + ' · ' + en.version })]),
        el('p', { class: 'orig' }, [el('span', { class: 'zh', text: game.title_zh }), ' · ' + game.pinyin]),
        el('p', { class: 'meta', text: game.year + ' · ' + game.genre + ' · ' + game.authors }),
        el('p', { class: 'blurb', text: game.blurb }),
        el('div', { class: 'actions-row' }, buttons)
      ])
    ]);
  }

  fetch('games.json')
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (cat) {
      box.textContent = '';
      for (const g of cat.games) box.appendChild(card(g));
    })
    .catch(function () {
      box.textContent = 'The library could not be loaded. Try reloading the page.';
    });
})();
