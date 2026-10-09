#!/usr/bin/env python3
"""Biuletyn BHP — zbiera wiadomości z oficjalnych źródeł do biuletyn.json (bez AI).

Uruchamiane codziennie przez GitHub Actions (.github/workflows/biuletyn.yml), można też ręcznie:
    python3 tools/biuletyn/zbierz.py            # zapisuje biuletyn.json w katalogu głównym repo
    python3 tools/biuletyn/zbierz.py --dry-run  # tylko wypisuje, co znalazł

Zasady:
  - źródła i słowa kluczowe są w tools/biuletyn/zrodla.json (zmiana źródła = edycja tego pliku),
  - tytuł i zajawka pochodzą wprost ze strony źródła (tytuł linku, meta description) — skrypt
    niczego nie streszcza ani nie dopisuje; każda pozycja ma link do oryginału,
  - błąd jednego źródła nie zatrzymuje pozostałych — trafia do sekcji "sources" w biuletyn.json,
  - plik zapisuje się tylko wtedy, gdy zmieniła się treść albo minęły 3 dni od ostatniego zapisu
    (żeby nie tworzyć codziennie pustych commitów).
Tylko biblioteka standardowa Pythona (3.9+).
"""
import datetime as dt
import email.utils
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CONF = Path(__file__).resolve().parent / 'zrodla.json'
OUT = ROOT / 'biuletyn.json'
KEEP_DAYS = 400          # jak długo trzymać pozycje
MAX_ITEMS = 700
NEW_PER_SOURCE = 15      # ile nowych artykułów na źródło pobierać w jednym przebiegu (grzecznie dla serwerów)
UA = 'Mozilla/5.0 (compatible; BHP-Audyt-Biuletyn/1.0; +https://tomekkulcz-source.github.io/bhp-audyt/)'
TODAY = dt.date.today()

MONTHS = {
    'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4, 'maja': 5, 'czerwca': 6, 'lipca': 7, 'sierpnia': 8,
    'września': 9, 'wrzesnia': 9, 'października': 10, 'pazdziernika': 10, 'listopada': 11, 'grudnia': 12,
    'styczeń': 1, 'luty': 2, 'marzec': 3, 'kwiecień': 4, 'maj': 5, 'czerwiec': 6, 'lipiec': 7, 'sierpień': 8,
    'wrzesień': 9, 'październik': 10, 'listopad': 11, 'grudzień': 12,
    'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12,
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'sept': 9, 'oct': 10, 'nov': 11, 'dec': 12,
}
MON_RE = '|'.join(sorted(MONTHS, key=len, reverse=True))
DATE_PATTERNS = [
    (re.compile(r'(20\d\d)-(\d\d)-(\d\d)'), lambda m: (int(m[1]), int(m[2]), int(m[3]))),
    (re.compile(r'\b(\d{1,2})[./](\d{1,2})[./](20\d\d)\b'), lambda m: (int(m[3]), int(m[2]), int(m[1]))),
    (re.compile(r'\b(\d{1,2})\s+(' + MON_RE + r')\.?,?\s+(20\d\d)\b', re.I), lambda m: (int(m[3]), MONTHS[m[2].lower()], int(m[1]))),
    (re.compile(r'\b(' + MON_RE + r')\.?\s+(\d{1,2}),?\s+(20\d\d)\b', re.I), lambda m: (int(m[3]), MONTHS[m[1].lower()], int(m[2]))),
]
CHEM_KW = ('reach', 'clp', 'chemiczn', 'substancj', 'rakotwórcz', 'mutagen', 'chemical', 'carcinogen')
PPOZ_KW = ('pożar', 'przeciwpożar', 'ewakuac', 'gaśnic')


def log(*a):
    print(*a, flush=True)


def fetch(url, accept='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', tries=2):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': accept, 'Accept-Language': 'pl,en;q=0.7'})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read(4_000_000)
                cs = r.headers.get_content_charset()
                if not cs:
                    m = re.search(rb'<meta[^>]+charset=["\']?([\w-]+)', raw[:4000], re.I)
                    cs = m.group(1).decode() if m else 'utf-8'
                return raw.decode(cs, errors='replace'), r.geturl()
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            last = e
            time.sleep(2 + 3 * i)
    raise last


def clean(s):
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))
    return re.sub(r'\s+', ' ', s).strip()


def cut(s, n=320):
    s = clean(s)
    if len(s) <= n:
        return s
    s = s[:n].rsplit(' ', 1)[0].rstrip(',;:–-')
    return s + '…'


def valid_date(y, m, d):
    try:
        x = dt.date(y, m, d)
    except ValueError:
        return None
    if x > TODAY + dt.timedelta(days=2) or x.year < 2015:
        return None
    return x.isoformat()


def all_dates(text):
    out = []
    for rx, conv in DATE_PATTERNS:
        for m in rx.finditer(text or ''):
            try:
                v = valid_date(*conv(m))
            except (KeyError, ValueError):
                v = None
            if v:
                out.append((m.start(), v))
    return sorted(out)


def find_date(text, near=None):
    """Pierwsza data w tekście, a z near=pozycja — data najbliższa tej pozycji."""
    ds = all_dates(text)
    if not ds:
        return None
    if near is None:
        return ds[0][1]
    return min(ds, key=lambda d: abs(d[0] - near))[1]


def rfc_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = email.utils.parsedate_to_datetime(s)
        return valid_date(d.year, d.month, d.day)
    except (TypeError, ValueError, IndexError):
        return find_date(s)


def item_id(url):
    return hashlib.sha1(url.encode()).hexdigest()[:12]


def norm(s):
    return clean(s).lower()


def matches(text, words):
    t = norm(text)
    return any(w in t for w in words)


class PageParser(HTMLParser):
    """Linki (href + tekst), meta tagi, kanały RSS i znaczniki <time> ze strony."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.meta, self.feeds, self.times = [], {}, [], []
        self._a = None
        self._title = None
        self.title = ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a' and a.get('href'):
            self._a = {'href': a['href'], 'text': '', 'title': a.get('title') or a.get('aria-label') or ''}
        elif tag == 'meta':
            k = (a.get('property') or a.get('name') or a.get('itemprop') or '').lower()
            if k and a.get('content') and k not in self.meta:
                self.meta[k] = a['content']
        elif tag == 'link' and 'alternate' in (a.get('rel') or '').lower() and re.search(r'(rss|atom)\+xml', a.get('type') or ''):
            self.feeds.append(a.get('href'))
        elif tag == 'time' and a.get('datetime'):
            self.times.append(a['datetime'])
        elif tag == 'title':
            self._title = ''

    def handle_endtag(self, tag):
        if tag == 'a' and self._a is not None:
            self.links.append(self._a)
            self._a = None
        elif tag == 'title' and self._title is not None:
            self.title = self._title
            self._title = None

    def handle_data(self, data):
        if self._a is not None:
            self._a['text'] += data
        if self._title is not None:
            self._title += data


def parse_page(text):
    p = PageParser()
    try:
        p.feed(text)
    except Exception:  # HTMLParser bywa wrażliwy na zepsuty HTML — bierzemy, co zdążył
        pass
    return p


def article_meta(url):
    """Tytuł, zajawka i data wprost ze strony artykułu (og:*, description, <time>)."""
    text, final = fetch(url)
    p = parse_page(text)
    m = p.meta
    title = clean(m.get('og:title') or p.title)
    lead = m.get('og:description') or m.get('description') or m.get('twitter:description') or ''
    date = None
    for k in ('article:published_time', 'datepublished', 'dc.date', 'dcterms.created', 'date', 'og:updated_time', 'article:modified_time'):
        if m.get(k):
            date = find_date(m[k])
            if date:
                break
    if not date:
        for t in p.times:
            date = find_date(t)
            if date:
                break
    if not date:
        body = re.sub(r'<(script|style)[\s\S]*?</\1>', ' ', text, flags=re.I)
        i = body.lower().find('<h1')
        date = find_date(clean(body[i:i + 6000] if i >= 0 else body[:20000]))
    return {'title': title, 'lead': cut(lead), 'date': date, 'url': final}


def parse_feed(text, base):
    root = ET.fromstring(text.encode('utf-8') if isinstance(text, str) else text)
    out = []
    for el in root.iter():
        tag = el.tag.split('}')[-1]
        if tag not in ('item', 'entry'):
            continue
        f = {}
        for c in el:
            ct = c.tag.split('}')[-1]
            if ct == 'link':
                f.setdefault('link', c.get('href') or (c.text or '').strip())
            elif ct in ('title', 'description', 'summary', 'pubDate', 'published', 'updated', 'date'):
                f.setdefault(ct, ''.join(c.itertext()))
        if f.get('link') and f.get('title'):
            out.append({
                'url': urllib.parse.urljoin(base, f['link'].strip()),
                'title': clean(f['title']),
                'lead': cut(f.get('description') or f.get('summary') or ''),
                'date': rfc_date(f.get('pubDate') or f.get('published') or f.get('date') or f.get('updated')),
            })
    return out


def from_html_list(src, text, base):
    rx = re.compile(src['link'], re.I)
    p = parse_page(text)
    seen, out = set(), []
    for a in p.links:
        href = urllib.parse.urljoin(base, html.unescape(a['href'].strip()))
        href = href.split('#')[0]
        if src.get('strip_query'):
            href = href.split('?')[0]
        if not rx.search(href):
            continue
        title = clean(a['text']) or clean(a['title'])
        if len(title) < 15:
            title = ''  # np. "Czytaj więcej" — tytuł weźmiemy ze strony artykułu
        # data często stoi tuż przy linku na liście — bierzemy najbliższą (bez tagów HTML)
        date, listed = None, False
        if href not in seen:
            seen.add(href)
            i = text.find(a['href'])
            if i >= 0:
                before = re.sub(r'<[^>]+>', ' ', text[max(0, i - 400): i])
                after = re.sub(r'<[^>]+>', ' ', text[i: i + 800])
                date = find_date(before + after, near=len(before))
                # "na liście" = data tuż przed linkiem albo zaraz za nim (pozycje menu tego nie mają)
                listed = bool(find_date(before[-250:]) or find_date(after[:160]))
        out.append({'url': href, 'title': title, 'lead': '', 'date': date, 'listed': listed if date else False})
    # ten sam artykuł bywa podlinkowany kilka razy (obrazek + tytuł) — zostaw wersję z tytułem
    best = {}
    for it in out:
        b = best.get(it['url'])
        if b is None:
            best[it['url']] = it
        else:
            if not b['title'] and it['title']:
                b['title'] = it['title']
            b['listed'] = b['listed'] or it['listed']
    if src.get('need_date'):  # pozycje menu nie mają daty na liście — artykuły mają
        best = {u: it for u, it in best.items() if it['listed']}
    return list(best.values())[:30]


def categorize(src, title, lead):
    cat = src.get('cat', 'wiadomosci')
    if cat in ('przepisy', 'projekty'):
        return cat
    t = norm(title + ' ' + lead)
    if cat != 'chemia' and any(k in t for k in CHEM_KW):
        return 'chemia'
    if any(k in t for k in PPOZ_KW):
        return 'ppoz'
    return cat


def collect_web(src, conf, known, skip):
    """Źródło typu html/rss → lista pozycji (nowe + już znane, odświeżone)."""
    words = [w.lower() for w in (src.get('only') or conf.get('slowa') or [])]
    if src['type'] == 'rss':
        feed_url = src['url']
        cands = parse_feed(fetch(feed_url, accept='application/rss+xml,application/atom+xml,application/xml,text/xml')[0], feed_url)
        via = 'rss'
    else:
        text, base = fetch(src['url'])
        cands, via = [], 'html'
        p = parse_page(text)
        rx = re.compile(src['link'], re.I)
        for f in p.feeds:  # kanał RSS na stronie — pewniejszy niż parsowanie HTML
            try:
                fu = urllib.parse.urljoin(base, f)
                got = [c for c in parse_feed(fetch(fu, accept='application/rss+xml,application/atom+xml,application/xml')[0], fu) if rx.search(c['url'])]
                if got:
                    cands, via = got, 'rss'
                    break
            except Exception as e:
                log(f'   kanał {f}: {e}')
        if not cands:
            cands = from_html_list(src, text, base)
    log(f'   {len(cands)} linków ({via})')
    out, fetched = [], 0
    for c in cands:
        iid = item_id(c['url'])
        if iid in known:
            out.append(known[iid])
            continue
        if iid in skip:
            continue
        if fetched >= NEW_PER_SOURCE:
            continue
        if not c['title'] or not c['lead'] or not c['date']:
            fetched += 1
            try:
                m = article_meta(c['url'])
                c['title'] = c['title'] or m['title']
                c['lead'] = c['lead'] or m['lead']
                # data ze strony artykułu jest pewniejsza niż zgadywana z sąsiedztwa linku na liście
                c['date'] = (m['date'] or c['date']) if via == 'html' else (c['date'] or m['date'])
                time.sleep(0.7)
            except Exception as e:
                log(f'   ! {c["url"]}: {e}')
        if not c['title']:
            continue
        if src.get('filter') and not matches(c['title'] + ' ' + c['lead'], words):
            skip.add(iid)  # nie na temat BHP — zapamiętaj, żeby nie pobierać ponownie
            continue
        guess = not c['date']
        it = {
            'id': iid, 'src': src['id'], 'cat': categorize(src, c['title'], c['lead']),
            'title': c['title'], 'lead': c['lead'] if c['lead'] and norm(c['lead']) != norm(c['title']) else '',
            'url': c['url'], 'date': c['date'] or TODAY.isoformat(), 'seen': TODAY.isoformat(),
        }
        if guess:
            it['dateGuess'] = True
        out.append(it)
    return out


def eli_kind(t):
    t = t.lower()
    if 'jednolitego tekstu' in t:
        return 'tj'
    if re.search(r'zmieniając|o zmianie|uchylając', t):
        return 'zm'
    return 'new'


def eli_ok(title, conf):
    """Akt dotyczy BHP: słowo z eli_slowa w tytule i żadnego z eli_bez (sprawy organizacyjne służb itp.)."""
    return matches(title, [w.lower() for w in conf.get('eli_slowa', [])]) and not matches(title, [w.lower() for w in conf.get('eli_bez', [])])


def collect_eli(src, conf, known):
    since = TODAY - dt.timedelta(days=src.get('days', 120))
    acts = []
    for y in sorted({since.year, TODAY.year}):
        j = json.loads(fetch(src['url'] + str(y), accept='application/json')[0])
        acts += j if isinstance(j, list) else j.get('items', [])
    log(f'   {len(acts)} aktów w roczniku')
    out, details = [], 0
    for a in acts:
        date = str(a.get('promulgation') or a.get('announcementDate') or '')[:10]
        title = a.get('title') or ''
        if not date or date < since.isoformat() or not eli_ok(title, conf):
            continue
        year, pos = a.get('year'), a.get('pos')
        addr = a.get('address') or f'WDU{year}{int(pos or 0):07d}'
        url = 'https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=' + addr
        iid = item_id(url)
        if iid in known and known[iid].get('inForce') is not None:
            out.append(known[iid])
            continue
        in_force = None
        if details < 40:
            details += 1
            try:
                d = json.loads(fetch(f'{src["url"]}{year}/{pos}', accept='application/json')[0])
                in_force = str(d.get('entryIntoForce') or d.get('validFrom') or '')[:10] or None
                time.sleep(0.3)
            except Exception as e:
                log(f'   ! szczegóły {addr}: {e}')
        out.append({
            'id': iid, 'src': src['id'], 'cat': 'przepisy', 'title': clean(title), 'lead': '',
            'url': url, 'date': date, 'seen': known.get(iid, {}).get('seen') or TODAY.isoformat(),
            'addr': a.get('displayAddress') or f'Dz.U. {year} poz. {pos}', 'type': a.get('type') or '',
            'kind': eli_kind(title), 'inForce': in_force,
        })
    return out


def main():
    dry = '--dry-run' in sys.argv
    conf = json.loads(CONF.read_text(encoding='utf-8'))
    old = {}
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text(encoding='utf-8'))
        except ValueError:
            old = {}
    known = {it['id']: it for it in old.get('items', [])}
    old_status = {s['id']: s for s in old.get('sources', [])}
    items = dict(known)
    skip = set(old.get('skip', []))
    status = []
    for src in conf['sources']:
        log(f'== {src["name"]} ({src["url"]})')
        st = {k: src.get(k) for k in ('id', 'name', 'full', 'home', 'cat')}
        prev = old_status.get(src['id'], {})
        try:
            got = collect_eli(src, conf, known) if src['type'] == 'eli' else collect_web(src, conf, known, skip)
            new = [g for g in got if g['id'] not in known]
            for g in got:
                items[g['id']] = g
            st.update(ok=True, found=len(got), new=len(new), lastOk=TODAY.isoformat())
            log(f'   OK: {len(got)} pozycji, nowych {len(new)}')
            for g in new[:8]:
                log(f'   + {g["date"]} {g["title"][:110]}')
        except Exception as e:
            st.update(ok=False, error=f'{type(e).__name__}: {e}'[:300], lastOk=prev.get('lastOk'))
            log(f'   BŁĄD: {st["error"]}')
        status.append(st)

    cutoff = (TODAY - dt.timedelta(days=KEEP_DAYS)).isoformat()
    ids = {s['id'] for s in conf['sources']}
    eli_ids = {s['id'] for s in conf['sources'] if s['type'] == 'eli'}
    lst = [it for it in items.values() if it['date'] >= cutoff and it['src'] in ids
           and (it['src'] not in eli_ids or eli_ok(it['title'], conf))]  # po zmianie słów kluczowych
    lst.sort(key=lambda it: (it['date'], it.get('seen', '')), reverse=True)
    lst = lst[:MAX_ITEMS]

    data = {'version': 1, 'generatedAt': dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'sources': status, 'items': lst, 'skip': sorted(skip)[-3000:]}
    strip = lambda d: json.dumps({**d, 'generatedAt': None, 'sources': [{**s, 'lastOk': None} for s in d.get('sources', [])]},
                                 ensure_ascii=False, sort_keys=True)
    changed = strip(data) != strip(old) if old else True
    stale = True
    if old.get('generatedAt'):
        try:
            last = dt.datetime.strptime(old['generatedAt'], '%Y-%m-%dT%H:%M:%SZ').date()
            stale = (TODAY - last).days >= 3
        except ValueError:
            pass
    ok = sum(1 for s in status if s['ok'])
    log(f'\nRazem {len(lst)} pozycji; źródła OK: {ok}/{len(status)}; zmiana treści: {changed}')
    if dry:
        return
    if changed or stale:
        OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        log(f'Zapisano {OUT.name}')
    else:
        log('Bez zmian — plik pozostaje bez zapisu')


if __name__ == '__main__':
    main()
