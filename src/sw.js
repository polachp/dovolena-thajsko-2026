// Service worker pro offline režim (od 12. 11. 2026). Šablona: src/sw.js, build.py z ní generuje sw.js v kořeni webu
// a doplní VERZE (otisk všech uložených souborů) a SOUBORY (co se uloží hned při první návštěvě). sw.js v kořeni needitovat.
//
// Strategie:
// - Stránky (index.html aktuální i starších verzí): nejdřív síť, když do 4 s neodpoví nebo není signál, uložená kopie.
// - Ostatní soubory webu (skripty s otiskem ?v=..., fonty, Leaflet, ikony): nejdřív uložená kopie, jinak síť a uložit.
// - Mapové dlaždice CARTO: ukládají se jen ty, které si už někdo zobrazil (žádné hromadné stahování), nejvýš 30 dní
//   (podmínky CARTO: cache v zařízení nejvýš 30 dní) a nejvýš MAX_DLAZDIC kusů. Dlaždice OSM se neukládají (OSM offline použití zakazuje).
var VERZE = '{{VERZE}}';
var SOUBORY = {{SOUBORY}};
var CACHE = 'thajsko-' + VERZE;
var CACHE_STRANKY = 'thajsko-stranky';
var CACHE_DLAZDICE = 'thajsko-dlazdice';
var MAX_DLAZDIC = 3000;
var STARI_DLAZDICE = 30 * 864e5;

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(SOUBORY); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (klice) {
    return Promise.all(klice.filter(function (k) {
      return k.indexOf('thajsko-') === 0 && k !== CACHE && k !== CACHE_STRANKY && k !== CACHE_DLAZDICE;
    }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

function sitSLimitem(req, ms) {
  return new Promise(function (ok, chyba) {
    var t = setTimeout(function () { chyba(new Error('timeout')); }, ms);
    fetch(req).then(function (r) { clearTimeout(t); ok(r); }, function (err) { clearTimeout(t); chyba(err); });
  });
}

function stranka(req) {
  return sitSLimitem(req, 4000).then(function (r) {
    if (r && r.ok) {
      var kopie = r.clone();
      caches.open(CACHE_STRANKY).then(function (c) { c.put(req.url.split('#')[0].split('?')[0], kopie); });
    }
    return r;
  }).catch(function () {
    var cista = req.url.split('#')[0].split('?')[0];
    return caches.match(cista).then(function (r) {
      return r || caches.match(req, { ignoreSearch: true });
    }).then(function (r) {
      return r || new Response('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
        '<p style="font-family:sans-serif;padding:24px">Tato stránka není uložená v telefonu a není připojení. Aktuální itinerář je na <a href="' +
        self.registration.scope + '">úvodní stránce</a>.</p>', { headers: { 'Content-Type': 'text/html; charset=utf-8' } });
    });
  });
}

function soubor(req) {
  return caches.match(req).then(function (r) {
    if (r) return r;
    return fetch(req).then(function (s) {
      if (s && s.ok) { var kopie = s.clone(); caches.open(CACHE_STRANKY).then(function (c) { c.put(req, kopie); }); }
      return s;
    });
  });
}

function prilisStara(r) {
  var d = Date.parse(r.headers.get('date') || '');
  return !d || Date.now() - d > STARI_DLAZDICE;
}

function orezDlazdice(c) {
  return c.keys().then(function (k) {
    if (k.length <= MAX_DLAZDIC) return;
    return Promise.all(k.slice(0, k.length - MAX_DLAZDIC).map(function (x) { return c.delete(x); }));
  });
}

function dlazdice(req) {
  return caches.open(CACHE_DLAZDICE).then(function (c) {
    return c.match(req).then(function (r) {
      if (r && !prilisStara(r)) return r;
      return fetch(req).then(function (s) {
        if (s && s.ok && s.type === 'cors') { c.put(req, s.clone()).then(function () { return orezDlazdice(c); }); }
        return s;
      }).catch(function () {
        if (r) { c.delete(req); }
        return Response.error();
      });
    });
  });
}

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  var url = new URL(req.url);
  if (url.hostname === 'basemaps.cartocdn.com' || /\.basemaps\.cartocdn\.com$/.test(url.hostname)) { e.respondWith(dlazdice(req)); return; }
  if (url.origin !== self.location.origin) return;
  if (req.mode === 'navigate') { e.respondWith(stranka(req)); return; }
  e.respondWith(soubor(req));
});

// stránka se může zeptat, co je uložené (záložka Více)
self.addEventListener('message', function (e) {
  if (!e.data || e.data.typ !== 'stav') return;
  caches.open(CACHE_DLAZDICE).then(function (c) { return c.keys(); }).then(function (k) {
    e.source.postMessage({ typ: 'stav', verze: VERZE, dlazdic: k.length });
  });
});
