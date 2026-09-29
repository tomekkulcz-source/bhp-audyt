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
`accident_cases`, `employees`, `recommendations`.
