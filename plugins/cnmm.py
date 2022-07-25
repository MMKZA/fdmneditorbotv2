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
    qlt_lst = []
    for a in soup.find_all('span', {'class': 'd'}):
        qlt_lst.append(a.text)
    sz_lst = []
    for a in soup.find_all('span', {'class': 'c'}):
        sz_lst.append(a.text)
    for s in url_lst:
        if "https://www.cmvipmembers.com/" in s:
            index = url_lst.index(s)
            del s
            del qlt_lst[index]
            del sz_lst[index]
        else:
            sz_lst = sz_lst
            qlt_lst = qlt_lst
            url_lst = url_lst
    #for s in szs_lst:
        #if s == "":
            #sz_lst.append("0 GB")
        #else:
            #sz_lst.append(s)
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
    kwd_st = ['https://yoteshinportal.cc/','https://vip.yoteshinportal.cc/', 'https://mega.nz/file/']
    for k in kwd_st:
        for m in max_lst:
            if k in m:
                cnmm_lst.append(m.split("|", 3)[0])
    prr_cnmm = cnmm_lst[0]
    max_lk = prr_cnmm.split("|", 3)[0]
    qlt_kwd = []
    max_qlt = ""
    for k in qlt_lst:
        if "" != k:
            qlt_kwd.append(k)
    for m in max_lst:
        for q in qlt_kwd:
            if q in m:
                max_qlt = m.split("|",3)[1]
    if max_qlt == "":
        max_qlt = "HD"
    avlb_lk = '\n'.join([str(lk) for lk in cnmm_lst])
    Trnl.sh2.update('Q2', avlb_lk)
    Trnl.sh2.update('H2', max_qlt)
    ytsn_lk = max_lk
    return ytsn_lk
