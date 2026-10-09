# TYMCZASOWE — diagnostyka struktury stron źródeł (usunąć po dostrojeniu)
import sys, re, urllib.parse
sys.path.insert(0, 'tools/biuletyn')
import zbierz as z
def show(url, filt=None, n=70):
    print('\n######', url)
    try:
        t, fin = z.fetch(url)
    except Exception as e:
        print('ERR', e); return
    p = z.parse_page(t)
    print('final:', fin, 'len', len(t), 'links', len(p.links), 'feeds', p.feeds, 'title', p.title[:80])
    k = 0
    for a in p.links:
        h = urllib.parse.urljoin(fin, a['href']); tx = z.clean(a['text']) or z.clean(a['title'])
        if filt and not re.search(filt, h + ' ' + tx, re.I): continue
        if len(tx) < 12: continue
        print('  ', tx[:70], '|', h[:230]); k += 1
        if k >= n: break
z.fetch.__defaults__ = z.fetch.__defaults__
show('https://www.ciop.pl/')
show('https://www.ciop.pl/CIOPPortalWAR/appmanager/ciop/pl?_nfpb=true&_pageLabel=P30001831423569409', None, 20)
show('https://www.gov.pl/web/rodzina/wiadomosci')
show('https://www.gov.pl/web/rodzina')
show('https://www.zus.pl/o-zus/aktualnosci')
show('https://www.zus.pl/')
show('https://www.gov.pl/web/gis/wiadomosci', None, 15)
for u in ['https://echa.europa.eu/pl/rss', 'https://echa.europa.eu/news-and-events/news-alerts/all-news/-/asset_publisher/yhAseXkvBI2u/rss', 'https://www.udt.gov.pl/', 'https://www.gov.pl/web/kgpsp/aktualnosci']:
    show(u, None, 15)
import socket; socket.setdefaulttimeout(90)
show('https://legislacja.gov.pl/', 'projekt', 20)
