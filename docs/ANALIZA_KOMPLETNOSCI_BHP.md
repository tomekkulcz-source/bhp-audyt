# Analiza kompletności aplikacji „BHP Audyt” jako narzędzia pracy specjalisty ds. BHP

Data analizy: 29.09.2026 · Wersja przeanalizowana: artefakt 2baa1745 (zgodna z `index.html` w repozytorium, 40 sekcji)

## 1. Punkt odniesienia

Aplikację porównałem z obowiązkami specjalisty wynikającymi z:

- **§ 2 ust. 1 rozporządzenia RM z 2.09.1997 r. w sprawie służby BHP** (Dz.U. 1997 nr 109 poz. 704 ze zm.) — katalog zadań służby BHP; § 3 i § 4 to uprawnienia (kontrola, zalecenia, wstrzymanie pracy, odsunięcie pracownika);
- **Kodeksu pracy, dział X**: art. 207–209¹ (obowiązki pracodawcy, koordynacja art. 208, pierwsza pomoc i ewakuacja), 226 (ORZ), 227 (pomiary), 229 (badania), 234–235² (wypadki, choroby zawodowe), 237¹¹–237¹³ (służba BHP, konsultacje, komisja BHP), 237³–237⁴ (szkolenia, instrukcje), 237⁶–237⁹ (ŚOI, odzież);
- rozporządzeń wykonawczych: szkolenia BHP (MGiP 27.07.2004), ustalanie okoliczności wypadków (RM 1.07.2009), pomiary czynników szkodliwych (MZ 2.02.2011), badania lekarskie (MZiOS 30.05.1996), ogólne przepisy BHP (MPiPS 26.09.1997), maszyny (MG 30.10.2002), prace szczególnie niebezpieczne, ppoż. (MSWiA 7.06.2010);
- praktyki zawodowej (literatura CIOP-PIB, PIP, PN-ISO 45001, PN-N-18002) — czyli tego, co realnie robi zewnętrzny specjalista obsługujący wielu klientów.

## 2. Werdykt

**Jako baza wiedzy i zestaw wzorów aplikacja jest bardzo kompletna** — w praktyce szersza niż większość komercyjnych programów BHP na rynku: 144 dokumenty w katalogu A–U, 149 edytowalnych wzorów rejestrów, checklista audytowa (~345 pytań), obchód, listy PIP/SANEPID/DTR/biuro/praca zdalna, kompendium wymogów, rejestr ~150 aktów prawnych, terminy przechowywania, normy i progi, ISO, GHS, znaki, pierwsza pomoc, profilaktyka, test wiedzy (1104 pytania), kalendarz obowiązków i roczny.

**Jako narzędzie do obsługi wielu klientów jednocześnie — jeszcze nie jest kompletne.** Główna przyczyna: dane są zorganizowane wokół *dokumentów* (każdy rejestr to osobna tabela), a nie wokół *klienta i jego pracowników*. Wiedza o terminach (np. częstotliwość szkoleń, pomiarów wg krotności NDS, badań) jest w aplikacji opisana, ale **nie jest automatycznie liczona** z danych. Brakuje też warstwy biznesowej (planowanie wizyt, rozliczenia, raportowanie klientowi, powiadomienia) i warstwy zgodności RODO dla danych, które specjalista przetwarza w imieniu klientów.

## 3. Pokrycie zadań z § 2 rozporządzenia o służbie BHP

| # | Zadanie (§ 2 ust. 1) | Pokrycie | Uwagi |
|---|---|---|---|
| 1 | Kontrole warunków pracy i przestrzegania przepisów | ✅ pełne | Checklista, obchód, M.1, raport PDF, zdjęcia, historia i powtarzające się uchybienia |
| 2 | Bieżące informowanie pracodawcy o zagrożeniach + wnioski | 🟡 częściowe | Jest wzór M.5; brak obiegu: wysłanie → potwierdzenie odbioru → termin → realizacja |
| 3 | Okresowa analiza stanu BHP (min. raz w roku) | 🟡 częściowe | Wzór M.2 wypełniany ręcznie; brak automatycznego generatora z danych klienta |
| 4–5 | Udział w planach modernizacji, ocena dokumentacji nowych inwestycji | ❌ brak | Brak listy kontrolnej opiniowania projektu/inwestycji |
| 6 | Udział w przekazywaniu do użytkowania obiektów i urządzeń | ❌ brak | Brak protokołu odbioru BHP obiektu/stanowiska/maszyny |
| 7 | Wnioski dot. procesów produkcyjnych | 🟡 | Tylko wzór M.5 |
| 8 | Wnioski dot. ergonomii | 🟡 | P.1, P.3; wiedza o OWAS/REBA/RULA jest, brak kalkulatorów |
| 9–10 | Udział w regulaminach/instrukcjach, opiniowanie instrukcji stanowiskowych | 🟡 | Wzory rejestrów zawierają tylko kilka instrukcji (E.1, E.4–E.8); brak biblioteki/generatora instrukcji stanowiskowych |
| 11 | Ustalanie okoliczności i przyczyn wypadków | 🟡 dobre | Kreator 6 kroków + protokół PDF + wpis do C.4; braki — zob. p. 4.4 |
| 12 | Rejestry wypadków, chorób zawodowych, wyniki pomiarów | ✅ | C.4–C.6, G.1, F.1–F.11 |
| 13 | Doradztwo w stosowaniu przepisów | ✅ pełne | Baza wiedzy |
| 14 | Udział w ocenie ryzyka zawodowego | 🟡 dobre | Tylko metoda Risk Score; zob. p. 4.3 |
| 15 | Doradztwo w doborze ŚOI | 🟡 | Rejestry H.1–H.6, brak powiązania ORZ → dobór ŚOI |
| 16 | Szkolenia BHP i adaptacja nowo zatrudnionych | 🟡 | Wzory A.1–A.10 + test; brak modułu organizacji szkoleń — zob. p. 4.2 |
| 17 | Konsultowanie rozwiązań BHP (art. 237¹¹ᵃ) | ❌ brak | Brak rejestru/protokołu konsultacji |
| 18 | Udział w pracach komisji BHP | 🟡 | Wzór M.4; brak harmonogramu posiedzeń (min. raz na kwartał) |
| 19 | Popularyzacja BHP | 🟡 | Test wiedzy; brak materiałów do przekazania pracownikom |
| 20–22 | Współpraca z PIP, PIS, lekarzem MP, SIP, związkami | 🟡 | Wzory skierowań i umowy z MP; brak rejestru korespondencji/kontroli zewnętrznych w formie modułu (jest wzór M.3) |
| 23 | Ocena maszyn i urządzeń | ✅ | Moduł Maszyny + terminy przeglądów/UDT |
| § 3 | Wstrzymanie pracy / odsunięcie pracownika | ❌ brak | Brak formularza z natychmiastowym zawiadomieniem pracodawcy |

## 4. Lista braków — uporządkowana wg priorytetu

### 🔴 PRIORYTET 1 — krytyczne dla obsługi wielu klientów

**4.1. Profil klienta (karta zakładu) i silnik wymagań**
Obecnie klient to nazwa + daty umowy + pole tekstowe „zakres usług”. Potrzebne:
- dane: NIP, REGON, PKD, adres siedziby i **lokalizacje/oddziały**, osoby kontaktowe (pracodawca, kadry, kierownicy), lekarz MP, rzeczoznawca ppoż., UDT;
- struktura zatrudnienia: liczba pracowników, w tym kobiety, młodociani, osoby z niepełnosprawnością, zleceniobiorcy, pracownicy tymczasowi, praca zmianowa/nocna, praca zdalna;
- kategoria ryzyka / stopa składki wypadkowej ZUS, rodzaje prac (PSN, na wysokości, CMR, czynniki biologiczne, ATEX, UDT, azbest, ADR);
- **automatyczne wyznaczenie obowiązków na podstawie profilu**, np.: służba BHP etatowa (>100 pracowników), komisja BHP (>250), możliwość samodzielnego wykonywania zadań przez pracodawcę (≤10, lub ≤50 przy kategorii ryzyka ≤3), regulamin pracy (≥50), rejestr CMR, dokument ATEX, IWA (≥10 ubezpieczonych), Z-10 itp. Na tej podstawie checklista, kalendarz i katalog dokumentów pokazują tylko to, co dotyczy danego klienta, a nie wszystko.

**4.2. Kartoteka pracowników klienta (centralna baza) — największy brak strukturalny**
Dziś te same osoby trzeba wpisywać osobno do A.3/A.4 (szkolenia), B.2/B.3 (badania), H.3/H.4 (ŚOI), D.3 (zapoznanie z ORZ), E.10 (instrukcje), J.5 i „Terminy uprawnień”. Potrzebne:
- jedna karta pracownika: stanowisko → powiązana ORZ i czynniki szkodliwe → wymagane badania, szkolenia, uprawnienia, ŚOI;
- **automatyczne terminy**: szkolenie okresowe wg grupy (pierwsze w ciągu 12 mies.; robotnicze co 3 lata, a przy PSN co rok; administracyjno-biurowe co 6 lat; kierownicy/pracodawcy/inżynieryjno-techniczni/służba BHP co 5 lat), badania okresowe z daty z orzeczenia, uprawnienia UDT/SEP z datą ważności;
- import listy pracowników z Excela/CSV (od kadr klienta) i eksport;
- zbiorcze akcje: skierowania na badania seryjnie (z czynnikami z ORZ), listy obecności, zaświadczenia A.2 seryjnie;
- matryca „pracownik × wymaganie” z kolorami (aktualne / wygasa / przeterminowane) — to jest pierwszy widok, o który pyta inspektor PIP.

**4.3. Plan pracy i rozliczenia z klientem**
- harmonogram wizyt wynikający z umowy (np. 1 wizyta w miesiącu), automatyczny roczny plan działalności (O.3) dla każdego klienta;
- **dziennik wizyt / ewidencja czynności** (data, czas, co zrobiono, potwierdzenie klienta) — dowód wykonania umowy i podstawa miesięcznego raportu;
- rozliczenia: stawka ryczałtowa/godzinowa, usługi dodatkowe (szkolenia, obsługa wypadku), kilometrówka, zestawienie do faktury (ew. integracja z programem do faktur/KSeF);
- miesięczny/kwartalny **raport dla klienta** z wykonanych czynności i otwartych zaleceń.

**4.4. Powiadomienia poza aplikacją**
Statusy terminów liczą się tylko po otwarciu aplikacji. Potrzebne: powiadomienia push/e-mail (np. 30/14/7 dni przed terminem), cotygodniowe podsumowanie, eksport terminów do kalendarza (ICS/Google Calendar). Przy kilkudziesięciu klientach to warunek, żeby nic nie przeoczyć.

**4.5. RODO — aplikacja przetwarza dane szczególnych kategorii**
Moduł wypadków zbiera PESEL, adres, opis obrażeń, dane o trzeźwości; rejestry zawierają orzeczenia lekarskie i narażenia. Specjalista jest wtedy **podmiotem przetwarzającym** (art. 28 RODO). Potrzebne:
- wzór umowy powierzenia przetwarzania danych dla klienta (brak w katalogu — O.4 to umowa usługowa);
- rejestr kategorii czynności przetwarzania (art. 30 ust. 2 RODO) prowadzony przez specjalistę;
- retencja: automatyczne przypomnienie o terminie przechowywania/usunięcia (dane o terminach już są w aplikacji — brakuje ich zastosowania do zapisanych danych);
- eksport kompletu danych klienta przy zakończeniu umowy (przekazanie dokumentacji) i trwałe usunięcie;
- informacja o miejscu przechowywania danych (Firebase / baza artefaktu), szyfrowanie, zabezpieczenie dostępu (PIN/biometria na urządzeniu mobilnym).

### 🟠 PRIORYTET 2 — ważne braki merytoryczne

**4.6. Wypadki przy pracy — uzupełnienie kreatora**
- licznik **14 dni** na sporządzenie protokołu (§ 9 rozp. RM z 1.07.2009) i uzasadnienie przekroczenia terminu;
- przy kwalifikacji **ciężki / śmiertelny / zbiorowy** (pole „Skutki” w kreatorze istnieje) — pilnowanie niezwłocznego zawiadomienia PIP i prokuratury (art. 234 § 2 KP) z generowaniem zawiadomienia (wzór C.11 jest, ale kreator go nie wywołuje);
- etap zapoznania poszkodowanego z protokołem (prawo do zgłoszenia zastrzeżeń, 5 dni roboczych na zatwierdzenie przez pracodawcę) z datami i przypomnieniami;
- generowanie **Z-KW** z danych sprawy (dziś osobny wzór C.2 do ręcznego wypełnienia) i przypomnienie o terminie przekazania do GUS;
- wariant dla **zleceniobiorcy / osoby niebędącej pracownikiem** (w sekcji referencyjnej opisany, w kreatorze brak — pole „Rodzaj zdarzenia” ma tylko dwie opcje);
- zdarzenia potencjalnie wypadkowe (near miss) jako szybkie zgłoszenie z telefonu (jest tylko rejestr C.6);
- automatyczne **wskaźniki wypadkowości** (Wc, Wci) na podstawie spraw i liczby pracowników z profilu klienta.

**4.7. Choroby zawodowe — brak modułu roboczego**
Jest wiedza i rejestr G.1, ale brak obsługi sprawy: zgłoszenie podejrzenia (PIS + PIP), udział w badaniu warunków pracy przez PIS, decyzja, działania profilaktyczne (art. 235 KP).

**4.8. Ocena ryzyka zawodowego — rozbudowa**
- dodatkowe metody: **PN-N-18002** (macierz 3- i 5-stopniowa — najczęściej stosowana w Polsce i najczęściej oczekiwana przez PIP), metoda wstępnej analizy zagrożeń (PHA), JSA;
- oceny szczegółowe: hałas/drgania (F.11 jest), chemiczna i CMR (L.3 — wzór), biologiczna (G.3 — wzór), **obciążenie fizyczne i ergonomia (OWAS/REBA/NIOSH jako kalkulatory)**, psychospołeczna (P.3 — wzór), ATEX, pole elektromagnetyczne;
- oceny dla grup szczególnych: kobiety w ciąży i karmiące (art. 179 KP), młodociani, osoby z niepełnosprawnością;
- śledzenie zapoznania każdego pracownika z ORZ (z kartoteki pracowników) i automatyczny termin przeglądu ORZ;
- plan działań korygujących (D.6) powiązany z zadaniami i terminami;
- biblioteka szablonów ORZ dla typowych stanowisk (biuro, magazynier, operator wózka, kierowca, spawacz, sprzedawca…) do kopiowania między klientami — ogromna oszczędność czasu.

**4.9. Szkolenia BHP — moduł organizacji szkoleń**
Planowanie terminów i grup, program wg grupy zawodowej (A.10), lista obecności, **egzamin** (test wiedzy już jest — wystarczy powiązać z uczestnikiem i wynikiem), seryjne zaświadczenia A.2 z numeracją, rejestr A.4 wypełniany automatycznie, instruktaż stanowiskowy z kartą A.1 i przypomnieniem o szkoleniu okresowym w ciągu 12 mies.

**4.10. Pomiary czynników szkodliwych — kalkulator terminów**
Wiedza o częstotliwościach jest w aplikacji, ale w „Terminach przeglądów” częstotliwość wpisuje się ręcznie. Potrzebny kalkulator wg rozp. MZ z 2.02.2011: z wyniku pomiaru (krotność NDS/NDN) wyliczany termin kolejnego pomiaru (>0,5 NDS — co rok; 0,1–0,5 NDS — co 2 lata; CMR odpowiednio co 3/6 mies.; <0,1 NDS — brak obowiązku przy braku zmian), plus rejestr i karta badań oraz udostępnienie wyników pracownikom.

**4.11. Zalecenia pokontrolne i uprawnienia specjalisty**
- jeden, zbiorczy **rejestr zaleceń** (z audytów, obchodów, wypadków, kontroli PIP/PIS, pomiarów) z odpowiedzialnym, terminem, statusem i dowodem realizacji — dziś są rozproszone (M.1, M.6, polecenia powypadkowe);
- rejestr **kontroli zewnętrznych** (PIP, PIS, PSP, UDT) z nakazami, wystąpieniami i terminami odpowiedzi do organu;
- formularz **wstrzymania pracy / odsunięcia pracownika** (§ 3 ust. 1 pkt 3–4 rozporządzenia) z zawiadomieniem pracodawcy;
- wniosek do pracodawcy o zagrożeniach (M.5) z potwierdzeniem odbioru.

**4.12. Brakujące wzory/rejestry**
- rejestr **konsultacji** w sprawach BHP (art. 237¹¹ᵃ KP) i protokół wyboru przedstawicieli pracowników;
- **protokół odbioru BHP** obiektu, pomieszczenia, stanowiska, maszyny (§ 2 pkt 6);
- lista kontrolna opiniowania dokumentacji inwestycji/modernizacji (§ 2 pkt 4–5);
- **koordynacja BHP przy pracy kilku pracodawców w jednym miejscu** (art. 208 KP): porozumienie o współpracy, wyznaczenie koordynatora, rejestr podwykonawców i firm zewnętrznych, instruktaż dla firm zewnętrznych;
- zezwolenia na pracę: **przestrzenie zamknięte**, prace na wysokości, prace gorące (I.7 jest), **LOTO** — procedura i karta blokad;
- instrukcje stanowiskowe dla typowych maszyn/prac (wózek widłowy, szlifierka, piła, spawanie, prasa, drabiny, magazyn, prace biurowe) — obecnie w rejestrach tylko kilka instrukcji ogólnych;
- plan BIOZ i informacja BIOZ — tylko jako wiedza; brak wzoru dla klientów budowlanych;
- harmonogram posiedzeń komisji BHP (min. raz na kwartał) z przypomnieniami;
- rejestr korespondencji z urzędami (PIP, PIS, ZUS, GUS).

**4.13. Generator rocznej analizy stanu BHP (M.2)**
Aplikacja ma już wszystkie dane: wyniki audytów i obchodów, sprawy wypadkowe, zalecenia, ORZ, terminy szkoleń/badań/pomiarów/przeglądów. Brakuje przycisku „Wygeneruj analizę stanu BHP za rok X” łączącego to w jeden dokument z wnioskami i planem na kolejny rok. To zwykle najbardziej czasochłonny dokument roczny — tu aplikacja może dać największą przewagę.

### 🟡 PRIORYTET 3 — usprawnienia pracy i skalowania

**4.14. Komunikacja z klientem**
- wysyłka raportu/protokołu e-mailem z aplikacji;
- panel klienta tylko do odczytu (terminy, zalecenia, dokumenty) albo przynajmniej link do udostępnienia;
- podpis odręczny na tablecie/telefonie: potwierdzenie zapoznania z ORZ, instrukcjami, instruktażem, protokołem kontroli (dziś pole „podpis” jest tekstowe).

**4.15. Aktualność prawa**
- data „stan prawny na dzień” przy każdym akcie i module;
- dziennik zmian w przepisach (co się zmieniło i których klientów to dotyczy);
- okresowy przegląd bazy (np. kwartalnie) — baza wiedzy jest duża, więc bez tego szybko się zdezaktualizuje.

**4.16. Architektura i wydajność**
- jeden plik `index.html` ma ~23 MB (sekcja „Kompendia” ok. 14 MB) — na telefonie w terenie to długie ładowanie; warto ładować kompendia i PDF-y dopiero na żądanie;
- tryb offline: service worker (`sw.js`) przechowuje samą aplikację, ale zapisy wymagają połączenia z bazą, a moduł PDF działa tylko w trybie lokalnym — audyt w hali bez zasięgu warto przetestować i dodać kolejkę zapisów offline;
- współpraca: brak kont dla asystenta/współpracownika i ról — to bariera przy rozwoju z jednej osoby do małej firmy BHP;
- widoki przekrojowe dla wszystkich klientów: „wszystkie przeterminowane badania / szkolenia / przeglądy” w jednej tabeli z filtrem po kliencie (Start częściowo to robi);
- kopia zapasowa całości danych jednym przyciskiem (eksport JSON/ZIP) i przywracanie.

**4.17. Drobne uzupełnienia merytoryczne**
- kalkulator IWA (informacja o danych do ustalenia składki wypadkowej, do 31 stycznia) i przypomnienie o sprawozdaniu GUS Z-10;
- kalkulator liczby ratowników/osób do pierwszej pomocy i ewakuacji oraz apteczek wg liczby pracowników i zmian;
- normy przydziału napojów i posiłków profilaktycznych — powiązanie z pomiarami mikroklimatu i temperaturą (N.1/N.2 są jako wzory);
- materiały dla pracowników (ulotki, plakaty, instrukcje pierwszej pomocy do wydruku).

## 5. Rekomendowana kolejność wdrożenia

1. **Profil klienta + kartoteka pracowników z automatycznymi terminami** (4.1, 4.2) — fundament; po nim większość pozostałych punktów to generowanie dokumentów z już istniejących danych.
2. **Powiadomienia + zbiorczy rejestr zaleceń + widok przekrojowy terminów** (4.4, 4.11, 4.16).
3. **RODO: umowa powierzenia, retencja, eksport/usunięcie danych klienta** (4.5) — zanim w bazie znajdą się dane wielu klientów.
4. **Dziennik wizyt, plan roczny i raport dla klienta, rozliczenia** (4.3).
5. **Uzupełnienie kreatora wypadków + moduł chorób zawodowych** (4.6, 4.7).
6. **ORZ: PN-N-18002, szablony stanowisk, oceny szczegółowe** (4.8) i **kalkulator pomiarów** (4.10).
7. **Moduł szkoleń** (4.9) i **generator analizy stanu BHP** (4.13).
8. Brakujące wzory (4.12), komunikacja z klientem (4.14), aktualność prawa (4.15), wydajność (4.16).

---
*Analiza na podstawie przeglądu kodu i treści aplikacji. Podstawy prawne podano według stanu znanego na dzień analizy — przed wdrożeniem konkretnych kalkulatorów terminów warto sprawdzić aktualne teksty jednolite w ISAP.*

## 6. Stan wdrożenia (aktualizowany)

| Etap | Zakres | Status |
|---|---|---|
| 1 | Profil klienta, wymagania z profilu, kartoteka pracowników (4.1, 4.2), pełna kopia zapasowa | ✅ wdrożone |
| 2 | Rejestr zaleceń i kontroli, terminy wszystkich klientów, eksport .ics, powiadomienie dzienne, wstrzymanie pracy i wnioski (4.4, 4.11) | ✅ wdrożone |
| 3 | RODO: umowa powierzenia, rejestr art. 30 ust. 2, retencja, zwrot i usunięcie danych (4.5) | ✅ wdrożone |
| 4 | Wizyty, raport miesięczny, plan roczny, rozliczenia (4.3) | ✅ wdrożone |
| 5 | Wypadki: terminy, zawiadomienia, Z-KW, wskaźniki; choroby zawodowe; near miss (4.6, 4.7) | ✅ wdrożone |
| 6 | ORZ: PN-N-18002, szablony stanowisk, grupy szczególne, zapoznanie; kalkulator pomiarów (4.8, 4.10) | ✅ wdrożone |
| 6a | Test wiedzy BHP przebudowany: pytania sytuacyjne zamiast pamięciowych (kody H, numery znaków), wyrównane dystraktory, poziomy pracownik/specjalista, uzasadnienie z podstawą prawną | ✅ wdrożone |
| 7 | Moduł szkoleń (plan z kartoteki, lista A.6, egzamin, zaświadczenia z numeracją, zapis do kartoteki), generator rocznej analizy stanu BHP (4.9, 4.13) | ✅ wdrożone |
| 8 | Wzory V.1–V.8 (konsultacje, odbiory, opiniowanie inwestycji, firmy zewnętrzne art. 208, LOTO, komisja BHP, korespondencja z urzędami, plan BIOZ); zestawienie stanu BHP dla klienta, wysyłanie plików z telefonu, podpisy na ekranie (szkolenia, zapoznanie z ORZ); dziennik zmian w przepisach z zadaniami u klientów; kalkulatory (IWA, osoby do pierwszej pomocy, posiłki i napoje); plakaty do wydruku; szybsze otwieranie aplikacji (4.12, 4.14–4.17) | ✅ wdrożone |

Poza zakresem pracy w samej aplikacji (wymagają serwera lub kont zewnętrznych): powiadomienia push/e-mail przy zamkniętej aplikacji, integracja z programem do faktur/KSeF, konta współpracowników z rolami.

Nie wdrożono (wymagają serwera albo zmiany sposobu wydawania): panel klienta online (zastąpiony zestawieniem PDF do wysłania), wydzielenie kompendiów (~14 MB) do osobnych plików — rozbiłoby to wersję lokalną jako jeden plik; zamiast tego aplikacja otwiera się z pamięci urządzenia i aktualizuje w tle. Instrukcje stanowiskowe typowych maszyn są w bibliotece instrukcji (E.1–E.92).
