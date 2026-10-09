# Wydawanie BHP Audyt — trzy wersje z jednego pliku

| Wersja | Źródło | Magazyn danych |
|---|---|---|
| Aplikacja (PWA, desktop + telefon) | `index.html` z gałęzi `main` (aktualizuje się sama) | Firebase / Firestore (logowanie Google) |
| Wersja lokalna | `index.html` zapisany jako `BHP_Audyt_wersja_lokalna.html` i otwarty z dysku | IndexedDB tej przeglądarki |
| claude.ai (artefakt) | `python3 tools/build_artifact.py` → `dist/bhp-audyt-claude.html` | baza artefaktu (`window.claude.use('db')`) |

Skrypt budujący usuwa z `index.html` nagłówek PWA, skrypty/konfigurację Firebase, rejestrację
service workera i wbudowane PDF-y kompendiów (limit 16 MB strony na claude.ai).

## Nowa kolekcja danych — lista kontrolna
1. `makeWtLocalDB` → dopisać nazwę do `STORES` i podnieść `DB_VERSION` (inaczej wersja lokalna nie utworzy magazynu).
2. `initCapsAndData` → `DB.collection('…').orderBy(…).onSnapshot(…)`.
3. `wtExportBackup` i `COLLECTIONS` w `wtImportBackup` → dopisać kolekcję (kopia zapasowa = jedyny sposób przenoszenia danych między wersjami).
4. Firebase → jeśli reguły Firestore wymieniają kolekcje z nazwy, dopisać nową.

## Kolekcje
`client_projects` (w tym `profile`, `reqState`), `todos`, `register_versions`, `checklist_snapshots`,
`item_photos`, `item_comments`, `notes`, `calendar_events`, `app_settings`, `pdf_files` (tylko lokalnie),
`risk_assessments`, `review_cards`, `machines`, `employee_permits_cards`, `custom_checklist_items`,
`accident_cases`, `employees`, `recommendations`, `visits`, `occupational_diseases`, `trainings`.

## Aktualizacja aplikacji (service worker)
`sw.js` (v3) otwiera `index.html` od razu z pamięci podręcznej i pobiera nową wersję w tle.
Gdy przyjdzie inna wersja (inny ETag/Last-Modified), aplikacja pokazuje pasek
„Dostępna nowa wersja — Odśwież”; kolejne uruchomienie startuje już z nowej wersji.
Zmiana `CACHE_NAME` w `sw.js` czyści starą pamięć przy następnym uruchomieniu.

## Ustawienia w `app_settings`
Wpisy dziennika zmian w przepisach zapisują się jako dokumenty `app_settings` z `key:'law_change'`
(bez nowej kolekcji).

## Biuletyn BHP (zakładka „Biuletyn BHP”)
Aktualizuje się sam, bez AI i bez kosztów:
1. **GitHub Actions** (`.github/workflows/biuletyn.yml`) codziennie ok. 6:20 uruchamia `tools/biuletyn/zbierz.py`.
2. Skrypt odwiedza źródła z `tools/biuletyn/zrodla.json` (Dziennik Ustaw przez API Sejmu, PIP, CIOP-PIB,
   EU-OSHA i inne), bierze tytuł, zajawkę (meta description / RSS) i datę wprost ze strony źródła
   i zapisuje `biuletyn.json` w katalogu głównym. Commit robi się tylko przy zmianie treści (albo co 3 dni).
3. GitHub Pages publikuje plik razem z aplikacją; aplikacja czyta go przy otwarciu zakładki
   (wersja lokalna i claude.ai — z `https://tomekkulcz-source.github.io/bhp-audyt/biuletyn.json`)
   i zapamiętuje ostatnią wersję w `localStorage` (działa bez internetu).

Wydanie = miesiąc kalendarzowy (numer `MM/RRRR`). „Nowe” = pozycje zebrane po poprzedniej wizycie w zakładce.
Stan źródeł widać w zakładce (panel „Źródła”) i w logu workflow. Zmiana/dodanie źródła = edycja
`zrodla.json` (typ `eli`, `rss` albo `html` z wyrażeniem `link` dla adresów artykułów; `filter: true` —
tylko wiadomości ze słowami z listy `slowa`). Ręczne uruchomienie: GitHub → Actions → Biuletyn BHP → Run workflow.
Test lokalny bez zapisu: `python3 tools/biuletyn/zbierz.py --dry-run`.
