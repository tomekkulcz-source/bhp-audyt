# TYMCZASOWE — diagnostyka struktury stron źródeł (usunąć po dostrojeniu)
import sys, re, urllib.parse
sys.path.insert(0, 'tools/biuletyn')
import zbierz as z
def show(url, filt, minlen=28, n=40):
    print('\n######', url)
    try:
        t, fin = z.fetch(url)
    except Exception as e:
        print('ERR', e); return
    p = z.parse_page(t)
    print('final:', fin, 'links', len(p.links), 'feeds', p.feeds)
    k = 0; seen = set()
    for a in p.links:
        h = urllib.parse.urljoin(fin, a['href']); tx = z.clean(a['text']) or z.clean(a['title'])
        if not re.search(filt, h, re.I) or len(tx) < minlen or h in seen: continue
        seen.add(h)
        i = t.find(a['href']); ctx = z.clean(t[max(0, i-300):i])[-80:]
        print('  ', tx[:80], '|', h[:260], '|| przed:', ctx); k += 1
        if k >= n: break
show('https://www.ciop.pl/', r'ciop\.pl', 20, 60)
show('https://www.gov.pl/web/rodzina/wiadomosci', r'/web/rodzina/', 25, 25)
show('https://www.gov.pl/web/rodzina', r'/web/rodzina/', 40, 25)
show('https://www.gov.pl/web/gis/wiadomosci', r'/web/gis/', 25, 12)
show('https://www.gov.pl/web/kgpsp/aktualnosci', r'/web/kgpsp/', 25, 12)
show('https://www.zus.pl/o-zus/aktualnosci', r'aktualnosci|/-/', 30, 25)
show('https://www.udt.gov.pl/', r'udt\.gov\.pl/(aktualnosci|wiadomosci|news|o-nas/aktualnosci)', 20, 15)
