import requests 
from bs4 import BeautifulSoup
import urllib
from lxml import html
import re
from trnl import Trnl

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


def google(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + urllib.parse.quote_plus(q) + '&sxsrf=ALiCzsbMQ9AgzAF9xpEvHzwZ-tA7dMO0WA%3A1661876002140&ei=IjcOY_CWCN2Q4-EPx_2rwAg&ved=0ahUKEwjwr5LG-u75AhVdyDgGHcf-CogQ4dUDCA4&uact=5&oq=Dr.+No+%281962%29+imdb&gs_lcp=Cgdnd3Mtd2l6EAMyBggAEB4QFjoFCAAQhgNKBAhBGABKBAhGGABQwQNY0QhgxAtoAHABeACAAcYDiAGTCJIBBzAuNC40LTGYAQCgAQHAAQE&sclient=gws-wiz'
    r = s.get(url, headers=headers_Get)
    tree = html.fromstring(r.content)
    soup = BeautifulSoup(r.text, "html.parser")
    href = []
    for h in soup.find_all('a', href=True):
        if 'https://www.imdb.com/title/tt' in h['href']:
            href.append(h['href'])
    imdb_lst = []
    for h in href:
        imdb_lst.append(re.search("(?P<url>https?://[^\s]+)", h).group("url"))
    for i in imdb_lst:
        imdb_tt_link = re.findall('[a-zA-Z]+://www\.imdb\.com/title/tt[0-9]+/',i)[0]
        imdb_id = imdb_tt_link.split('/')[-2]
        Trnl.sh2.update('M7',imdb_id)
    return imdb_id
