import requests
from bs4 import BeautifulSoup
import re
from trnl import Trnl
from lxml import html

def shweflix(web_url):
    web_req = requests.get(web_url)
    tree = html.fromstring(web_req.content)
    web_req.encoding = web_req.apparent_encoding
    web_html = web_req.text
    soup = BeautifulSoup(web_html, 'html.parser')
    if "shweflix" in web_url:
        urls_lst = []
        for a in soup.select('div > div.entry-content > div.wp-block-essential-blocks-advanced-tabs.alignwide > div > div > div.eb-tabs-contents > div:nth-child(3) > div > div > div > a'):
            urls_lst.append(a['href'])
        txt_lst = []
        for x in tree.xpath('///div/div[3]/div[2]/div/div/div[2]/div[3]/div/div/div/a'):
            txt_lst.append(x.text)
        qlt_lst = []
        sz_lst = []
        for t in txt_lst:
            qlt_lst.append(t.split('[')[0].strip())
            sz_lst.append(t.split('[')[-1].replace(']',''))
        gb_lst = ['GB', 'Gb', 'gb' 'gB']
        mb_lst = ['MB', 'Mb', 'mb' 'mB']
        szgb_lst = []
        for v in sz_lst:
           szspl = re.findall('(\d+|[A-Za-z]+)', v)
           szunt = szspl[len(szspl)-1]
           for g in gb_lst:
              if szunt in g:
                 szgb_lst.append(float("{:.2f}".format(float(v.replace(szunt, "").strip()))))
           for m in mb_lst:
              if szunt in m:
                 szgb_lst.append(float("{:.2f}".format(float(v.replace(szunt, "").strip()) / 1024)))
        all_lst = list(range(0,len(szgb_lst)))
        for i in all_lst:
            all_lst[i] = ("{} | {} | {}".format(url_lst[i],qlt_lst[i],str(szgb_lst[i])+"GB"))
        avlb_lk = '\n'.join([str(lk) for lk in all_lst])
        indices = [v for i, v in enumerate(szgb_lst) if v < 2]
        max_sz = float("{:.2f}".format(max(indices)))
        for m in szgb_lst:
            if max_sz == m:
                index = szgb_lst.index(m)
        max_qlt = qlt_lst[index]
        Trnl.sh2.update('H2', max_qlt)
        lk0 = urls_lst[index]
        web_req = requests.get(lk0)
        web_req.encoding = web_req.apparent_encoding
        web_html = web_req.text
        soup = BeautifulSoup(web_html, 'html.parser')
        hrf_lst = []
        for s in soup.find_all('a', href=True):
            hrf_lst.append(s)
        for h in hrf_lst:
            if 'gdtot.sbs/file/' in str(h):
                lk1 = h['href']
        return [avlb_lk, lk1]
