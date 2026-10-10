#!/usr/bin/env python3
"""Buduje wersję BHP Audyt na claude.ai (artefakt) z jednego źródła: index.html.

index.html obsługuje dwie z trzech wersji aplikacji:
  - aplikację (PWA desktop + telefon, https) — zapis w Firebase po zalogowaniu Google,
  - wersję lokalną (plik otwarty z dysku) — zapis w IndexedDB tej przeglądarki.
Wersja na claude.ai to ten sam kod, ale:
  - bez <head> z manifestem PWA i bez skryptów/konfiguracji Firebase (claude.ai ma
    własną bazę — window.claude.use('db') — i sam dokłada szkielet dokumentu),
  - bez rejestracji service workera,
  - bez wbudowanych PDF-ów kompendiów (~14 MB), żeby zmieścić się w limicie rozmiaru
    strony — w ich miejscu pojawia się informacja o wersji lokalnej,
  - z wklejonym stanem Biuletynu BHP (biuletyn.json) — claude.ai nie pozwala go pobrać z internetu.

Użycie:  python3 tools/build_artifact.py [wyjście]   (domyślnie dist/bhp-audyt-claude.html)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'index.html'
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'dist' / 'bhp-audyt-claude.html'

CLOUD_NOTE = ('<div class="wt-pdf-clouddisabled" style="margin:0;">To kompendium jest dostępne tylko '
              'w wersji lokalnej tego narzędzia (plik BHP_Audyt_wersja_lokalna.html otwarty na Twoim '
              'komputerze) — w wersji na claude.ai plik został pominięty, aby zmieścić się w limicie '
              'rozmiaru strony.</div>')


def build(s: str) -> str:
    # 1) Nagłówek PWA: wszystko przed <title> (szkielet doda claude.ai).
    i = s.index('<title>')
    s = '\n' + s[i:]
    # 2) Skrypty i konfiguracja Firebase + zamknięcie </head><body>.
    a = s.index('<script src="https://www.gstatic.com/firebasejs/')
    b = s.index('<body>\n', a) + len('<body>\n')
    s = s[:a] + s[b:]
    # 3) Rejestracja service workera i zamknięcie dokumentu.
    a = s.rindex("<script>\nif ('serviceWorker' in navigator)")
    s = s[:a] + '\n'
    # 4) PDF-y kompendiów zastąpione informacją o wersji lokalnej.
    s, n = re.subn(r'<div class="wt-pdf-actions"><button class="wt-btn primary" data-action="openstatic"'
                   r'[^>]*data-src="data:application/pdf;base64,[^"]*">Otwórz</button></div>', CLOUD_NOTE, s)
    if n == 0:
        raise SystemExit('Nie znaleziono PDF-ów kompendiów — sprawdź strukturę sekcji sec-kompendia.')
    # 5) Biuletyn BHP: claude.ai blokuje pobieranie biuletyn.json z internetu, więc wklejamy jego
    #    bieżący stan (aktualny na dzień budowania; codzienne nowości są tylko w aplikacji PWA).
    bt = ROOT / 'biuletyn.json'
    if bt.exists():
        data = json.loads(bt.read_text(encoding='utf-8'))
        data.pop('skip', None)
        snap = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
        marker = '<script>\n/* ---------------- Biuletyn BHP ----------------'
        if marker not in s:
            raise SystemExit('Nie znaleziono modułu Biuletynu BHP w index.html.')
        s = s.replace(marker, '<script>window.WT_BT_SNAPSHOT=' + snap + ';</script>\n' + marker, 1)
    return s


def main():
    out = build(SRC.read_text(encoding='utf-8'))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(out, encoding='utf-8')
    mb = len(out.encode('utf-8')) / 1024 / 1024
    print(f'{OUT} — {mb:.1f} MB')
    if mb > 15.5:
        raise SystemExit('UWAGA: plik zbliża się do limitu 16 MB strony na claude.ai.')


if __name__ == '__main__':
    main()
