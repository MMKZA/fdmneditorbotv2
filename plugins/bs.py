import requests
from bs4 import BeautifulSoup
import re
from trnl import Trnl
import json
from json2html import *

def bs(web_url):
    web_req = requests.get(web_url)
    # override encoding by real educated guess as provided by chardet
    web_req.encoding = web_req.apparent_encoding
    # access the data
    web_html = web_req.text
    soup = BeautifulSoup(web_html, 'html.parser')
    urls_lst = []
    for a in soup.find_all('a', href=True):
        urls_lst.append(a['href'])
    url_lst = [x for x in urls_lst if x.startswith('https://burmesesubtitles.com/links/')]
    qlt_lst = []
    for a in soup.find_all("strong", {"class": "quality"}):
        qlt_lst.append(a.text)
    sz_lst = []
    for a in soup.select('td:nth-child(4)'):
        sz_lst.append(a.text)
    sv_lst = []
    for a in soup.select('td:nth-child(2)'):
        sv_lst.append(a.text)
    gb_lst = ['GB', 'Gb', 'gb' 'gB']
    mb_lst = ['MB', 'Mb', 'mb' 'mB']
    szgb_lst = []
    for v in sz_lst:
        szspl = re.findall('(\d+|[A-Za-z]+)', v)
        szunt = szspl[len(szspl) - 1]
        for g in gb_lst:
            if szunt in g:
                szgb_lst.append(float("{:.2f}".format(float(v.replace(szunt, "").strip()))))
        for m in mb_lst:
            if szunt in m:
                szgb_lst.append(float("{:.2f}".format(float(v.replace(szunt, "").strip()) / 1024)))
    all_lst = list(range(0, len(szgb_lst)))
    for i in all_lst:
        all_lst[i] = ("{} | {} | {} | {}".format(url_lst[i], sv_lst[i], qlt_lst[i], str(szgb_lst[i]) + "GB"))
    indices = [v for i, v in enumerate(szgb_lst) if v < 2]
    max_sz = float("{:.2f}".format(max(indices)))
    max_lst = list(filter(lambda x: str(max_sz) + "GB" in x, all_lst))
    sv_kw = ['GDrive', 'Mega']
    max_qlt = ""
    for m in max_lst:
        for s in sv_kw:
            if s in m:
                max_qlt = m.split("|", 4)[2]
    if max_qlt == "":
        max_qlt = "HD"
    avlb_lst = []
    for s in sv_kw:
        for a in all_lst:
            if s in a:
                avlb_lst.append(a)
    avlb_lk = '\n'.join([str(lk) for lk in avlb_lst])
    max_avlb = []
    for m in max_lst:
        if 'GDrive' in m:
            max_avlb.append(m)
        elif 'Mega' in m:
            max_avlb.append(m)
    max_lks = '\n'.join([str(lk) for lk in max_avlb])
    Trnl.sh2.update('Q2', avlb_lk)
    Trnl.sh2.update('H2', max_qlt)
    try:
        gdrv = max_avlb[1].split("|",4)[0]
        gdrv_req = requests.get(gdrv)
        gdrv_req.encoding = gdrv_req.apparent_encoding
        gdrv_html = gdrv_req.text
        soup = BeautifulSoup(gdrv_html, 'html.parser')
        href_mega = []
        for a in soup.find_all('a', href=True):
            href_mega.append(a['href'])
        for h in href_mega:
            if 'https://gd.burmesesubtitles.com' in h:
                max_lk = h
        return [max_lks, max_lk]
    except:
        return [max_lks]