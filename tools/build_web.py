#!/usr/bin/env python3
"""Buduje wersję webową BHP Audyt do Cloudflare Pages → folder site/.

Cloudflare Pages przyjmuje pliki do 25 MiB, a index.html z wbudowanymi kompendiami PDF ma ~29 MB.
Dlatego kompendia trafiają do site/kompendia/*.pdf (aplikacja pobiera je dopiero przy otwarciu —
wtOpenStaticPdf obsługuje zarówno data: URI, jak i zwykły adres). Wersja lokalna (jeden plik HTML)
i build na claude.ai (tools/build_artifact.py) zostają bez zmian.

Uruchamia go Cloudflare Pages przy każdym pushu (Build command: python3 tools/build_web.py,
Build output directory: site). Można też lokalnie: python3 tools/build_web.py && python3 -m http.server -d site
"""
import base64, hashlib, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'site'
LIMIT = 25 * 1024 * 1024
STATIC = ['sw.js', 'manifest.json', 'icon-180.png', 'icon-192.png', 'icon-512.png', 'biuletyn.json']


def slug(t):
    t = t.lower()
    for a, b in zip('ąćęłńóśźż', 'acelnoszz'):
        t = t.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / 'kompendia').mkdir(parents=True)
    s = (ROOT / 'index.html').read_text(encoding='utf-8')
    n = 0

    def pdf(m):
        nonlocal n
        title, b64 = m.group(1), m.group(2)
        data = base64.b64decode(b64)
        name = slug(title)[:60] + '-' + hashlib.sha1(data).hexdigest()[:8] + '.pdf'
        (OUT / 'kompendia' / name).write_bytes(data)
        n += 1
        return 'data-title="' + title + '" data-src="kompendia/' + name + '"'

    s = re.sub(r'data-title="([^"]*)" data-src="data:application/pdf;base64,([A-Za-z0-9+/=]+)"', pdf, s)
    if n == 0:
        sys.exit('Nie znaleziono kompendiów PDF w index.html — sprawdź strukturę sec-kompendia.')
    (OUT / 'index.html').write_text(s, encoding='utf-8')
    for f in STATIC:
        if (ROOT / f).exists():
            shutil.copy2(ROOT / f, OUT / f)
    # nagłówki Cloudflare: strona zawsze świeża (service worker i tak trzyma kopię offline),
    # kompendia mają w nazwie skrót treści, więc mogą być w pamięci podręcznej długo
    (OUT / '_headers').write_text(
        '/\n  Cache-Control: no-cache\n'
        '/index.html\n  Cache-Control: no-cache\n'
        '/sw.js\n  Cache-Control: no-cache\n'
        '/biuletyn.json\n  Cache-Control: no-cache\n'
        '/kompendia/*\n  Cache-Control: public, max-age=31536000, immutable\n'
        '/*\n  X-Robots-Tag: noindex, nofollow\n', encoding='utf-8')
    big = [p for p in OUT.rglob('*') if p.is_file() and p.stat().st_size > LIMIT]
    if big:
        sys.exit('Pliki ponad 25 MiB (limit Cloudflare Pages): ' + ', '.join(str(p.relative_to(OUT)) for p in big))
    size = (OUT / 'index.html').stat().st_size / 1e6
    print(f'site/ gotowe — index.html {size:.1f} MB, kompendia: {n}')


if __name__ == '__main__':
    main()
