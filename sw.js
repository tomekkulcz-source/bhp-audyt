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
const CACHE_NAME = 'bhp-audyt-v2';
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

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
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
