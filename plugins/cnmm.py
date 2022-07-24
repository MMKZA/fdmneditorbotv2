import requests
from bs4 import BeautifulSoup
import re
from trnl import Trnl


def cnmm(web_url):
    web_req = requests.get(web_url)
    web_req.encoding = web_req.apparent_encoding
    web_html = web_req.text
    soup = BeautifulSoup(web_html, 'html.parser')
    urls_lst = []
    url_lst = []
    for a in soup.find_all('li', {'class': 'elemento'}):
        urls_lst.append(a)
    url_cmb = ''.join(map(str, urls_lst))
    soup = BeautifulSoup(url_cmb, 'html.parser')
    for a in soup.find_all('a', href=True):
        url_lst.append(a['href'])
    del url_lst[0]
    qlt_lst = []
    for a in soup.find_all('span', {'class': 'd'}):
        qlt_lst.append(a.text)
    del qlt_lst[0]
    sz_lst = []
    for a in soup.find_all('span', {'class': 'c'}):
        sz_lst.append(a.text)
    del sz_lst[0]
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
        all_lst[i] = ("{}|{}|{}".format(url_lst[i], qlt_lst[i], str(szgb_lst[i]) + "GB"))
    indices = [v for i, v in enumerate(szgb_lst) if v < 2]
    max_sz = float("{:.2f}".format(max(indices)))
    max_lst = list(filter(lambda x: str(max_sz) + "GB" in x, all_lst))
    cnmm_lst = []
    max_qlt = ''
    kwd_st = ['https://yoteshinportal.cc/', 'https://mega.nz/file/']
    for k in kwd_st:
        for m in max_lst:
            if k in m:
                cnmm_lst.append(m.split("|", 3)[0])
                max_qlt = m.split("|", 3)[1]
    prr_cnmm = cnmm_lst[0]
    max_lk = prr_cnmm.split("|", 3)[0]
    avlb_lk = '\n'.join([str(lk) for lk in cnmm_lst])
    Trnl.sh2.update('Q2', avlb_lk)
    Trnl.sh2.update('H2', max_qlt)
    ytsn_lk = max_lk
    return ytsn_lk
