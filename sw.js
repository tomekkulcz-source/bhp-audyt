// Service worker dla BHP Audyt — wersja PWA (instalowalna na ekranie głównym).
// Strategia "network-first": online zawsze pobiera najnowszą wersję i uaktualnia
// pamięć podręczną w tle; offline korzysta z ostatniej zapisanej wersji, żeby
// aplikacja w ogóle się otworzyła bez połączenia z internetem.
//
// {cache:'no-store'} na fetchu jest KLUCZOWE — bez tego "network-first" był tylko
// pozorny: fetch() domyślnie i tak może dostać odpowiedź z dyskowego cache
// przeglądarki (Cache-Control z GitHub Pages/CDN), więc zwykłe odświeżenie strony
// (nawet twarde, Cmd+Shift+R) potrafiło pokazywać starą wersję appki, mimo że
// service worker "łączył się z siecią" — realny incydent użytkownika: po
// wdrożeniu nowej funkcji w panelu klienta nie było jej widać nawet po twardym
// odświeżeniu, zniknęło dopiero w oknie prywatnym (bez zainstalowanego SW).
//
// v3: strona główna (index.html, ~23 MB) otwiera się od razu z pamięci podręcznej, a nowa
// wersja pobiera się w tle ("stale-while-revalidate"). Gdy w tle przyjdzie inna wersja niż
// zapisana, service worker zapisuje ją i wysyła do otwartych kart komunikat 'wt-update' —
// aplikacja pokazuje pasek „Dostępna nowa wersja — Odśwież”. Kolejne otwarcie i tak startuje
// już z nowej wersji. Pozostałe pliki (ikony, manifest) — jak dotąd network-first.
const CACHE_NAME = 'bhp-audyt-v3';
const CORE_ASSETS = ['./', './index.html', './manifest.json', './icon-192.png', './icon-512.png'];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(CORE_ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(names => Promise.all(
      names.filter(n => n !== CACHE_NAME).map(n => caches.delete(n))
    )).then(() => self.clients.claim())
  );
});

function isAppPage(request) {
  if (request.mode === 'navigate') return true;
  const url = new URL(request.url);
  return url.origin === self.location.origin && /\/(index\.html)?$/.test(url.pathname);
}

function versionTag(response) {
  return response.headers.get('etag') || response.headers.get('last-modified') || '';
}

async function refreshPage(request, cached) {
  const cache = await caches.open(CACHE_NAME);
  const fresh = await fetch(request, {cache: 'no-store'});
  if (!fresh || !fresh.ok) return;
  let changed;
  const a = versionTag(fresh), b = versionTag(cached);
  if (a && b) changed = a !== b;
  else changed = (await fresh.clone().text()) !== (await cached.clone().text());
  if (!changed) return;
  await cache.put(request, fresh.clone());
  await cache.put('./index.html', fresh.clone());
  const clients = await self.clients.matchAll({type: 'window'});
  clients.forEach(c => c.postMessage({type: 'wt-update'}));
}

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  if (isAppPage(event.request)) {
    event.respondWith((async () => {
      const cached = await caches.match(event.request, {ignoreSearch: true}) || await caches.match('./index.html');
      if (cached) {
        event.waitUntil(refreshPage(event.request, cached).catch(() => {}));
        return cached;
      }
      const response = await fetch(event.request, {cache: 'no-store'});
      const copy = response.clone();
      caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
      return response;
    })());
    return;
  }
  event.respondWith(
    fetch(event.request, {cache: 'no-store'})
      .then(response => {
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
        return response;
      })
      .catch(() => caches.match(event.request).then(cached => cached || caches.match('./index.html')))
  );
});
