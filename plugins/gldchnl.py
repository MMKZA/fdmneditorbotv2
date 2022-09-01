import requests
from bs4 import BeautifulSoup
import re
from trnl import Trnl

def gldchnl(gld_url):
    web_req = requests.get(gld_url)
    web_req.encoding = web_req.apparent_encoding
    web_html = web_req.text
    soup = BeautifulSoup(web_html, 'html.parser')
    urls_lst = []
    for a in soup.find_all('a', href=True):
        urls_lst.append(a['href'])
    url_lst = [x for x in urls_lst if x.startswith('https://goldchannel.net/links/')]
    qlt_lst = []
    for a in soup.find_all("strong", {"class": "quality"}):
        qlt_lst.append(a.text)
    sz_lst = []
    for a in soup.select('td:nth-child(4)'):
        sz_lst.append(a.text)
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
        all_lst[i] = ("{} | {} | {}".format(url_lst[i], qlt_lst[i], str(szgb_lst[i]) + "GB"))
    indices = [v for i, v in enumerate(szgb_lst) if v < 2]
    max_sz = float("{:.2f}".format(max(indices)))
    max_lst = list(filter(lambda x: str(max_sz) + "GB" in x, all_lst))
    qlt_kw = ['G Drive ', 'Mega ']
    max_qlt = ""
    for m in max_lst:
        for q in qlt_kw:
            if q in m:
                max_qlt = m.split("|", 3)[1].replace(q, "").strip()
    if max_qlt == "":
        max_qlt = "HD"
    kwd_st = ['G Drive', 'Mega']
    avlb_lst = []
    for k in kwd_st:
        for a in all_lst:
            if k in a:
                avlb_lst.append(a)
    gdrv_lst = []
    for al in all_lst:
        if 'G Drive' in al:
            gdrv = al.split("|", 3)[0].strip()
            gdrv_req = requests.get(gdrv)
            gdrv_req.encoding = gdrv_req.apparent_encoding
            gdrv_html = gdrv_req.text
            soup = BeautifulSoup(gdrv_html, 'html.parser')
            for a in soup.find_all('a', href=True):
                href_lst.append(a['href'])
            for h in href_lst:
                if 'followup=' in h:
                    dllk = h.split('followup=')[1]
                    gdrv_lst.append('{} | {} | {}'.format(dllk,al.split("|", 3)[1].strip(),al.split("|", 3)[2].strip()))
                if 'followup=' not in h:
                    if 'https://drive.google.com/file/d/' in h:
                        dllk = h
                        gdrv_lst.append('{} | {} | {}'.format(dllk,al.split("|", 3)[1].strip(),al.split("|", 3)[2].strip()))
    avlb_lk = '\n'.join([str(lk) for lk in avlb_lst])
    dllk = ''
    for m in max_lst:
        if 'G Drive' in m:
            max_gdrv = m.split("|", 3)[0].strip()
            gdrv_req = requests.get(max_gdrv)
            gdrv_req.encoding = gdrv_req.apparent_encoding
            gdrv_html = gdrv_req.text
            soup = BeautifulSoup(gdrv_html, 'html.parser')
            href_lst = []
            for a in soup.find_all('a', href=True):
                href_lst.append(a['href'])
            for h in href_lst:
                if 'followup=' in h:
                    dllk = h.split('followup=')[1]
                if 'followup=' not in h:
                    if 'https://drive.google.com/file/d/' in h:
                        dllk = h
        elif 'Mega' in m:
            max_mega = m.split("|", 3)[0].strip()
            dllk = max_mega
    Trnl.sh2.update('Q2', avlb_lk)
    Trnl.sh2.update('H2', max_qlt)
    return gdrv_lst
