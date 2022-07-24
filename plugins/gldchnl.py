import requests
from bs4 import BeautifulSoup
import re
from trnl import Trnl

def gldchnl(gld_url):
    urls_lst = []
    for a in soup.find_all('a', href=True):
        urls_lst.append(a['href'])
    url_lst = [x for x in urls_lst if x.startswith('https://goldchannel.net/links/')]
    qlt_lst = []
    for a in soup.find_all("strong", {"class": "quality"}):
        qlt_lst.append(a.text)
    sz_lst = []
    table = ''
    for a in soup.find_all('div', {'class': 'links_table'}):
        table = a.text
    sttrm1080_lst = ['G Drive FHD 1080pMyanmar', 'Mega FHD 1080pMyanmar']
    sttrm720_lst = ['G Drive HD 720pMyanmar', 'Mega HD 720pMyanmar']
    sttrm480_lst = ['G Drive SD 480pMyanmar', 'Mega SD 480pMyanmar']
    gb_lst = ['GB', 'Gb', 'gb', 'gB']
    mb_lst = ['MB', 'Mb', 'mb', 'mB']
    for x in gb_lst:
        if x in table:
            entrmGB = x
    for x in mb_lst:
        if x in table:
            entrmMB = x
    sz_lst = []
    for k in sttrm1080_lst:
        if k in table:
            if entrmGB in table:
                size1080 = (table.split(k))[1].split(entrmGB)[0]
            if "Myanmar" in size1080:
                size1080 = float("{:.2f}".format(float((table.split(k))[1].split(entrmMB)[0]) / 1024))
            else:
                size1080 = float(size1080)
            sz_lst.append(size1080)

    for k in sttrm720_lst:
        if k in table:
            if entrmGB in table:
                size720 = (table.split(k))[1].split(entrmGB)[0]
            if "Myanmar" in size720:
                size720 = float("{:.2f}".format(float((table.split(k))[1].split(entrmMB)[0]) / 1024))
            else:
                size720 = float(size720)
            sz_lst.append(size720)
    for k in sttrm480_lst:
        if k in table:
            if entrmGB in table:
                size480 = (table.split(k))[1].split(entrmGB)[0]
            if "Myanmar" in size480:
                size480 = "{:.2f}".format(float((table.split(k))[1].split(entrmMB)[0]) / 1024)
            else:
                size480 = float(size480)
            sz_lst.append(float(size480))

    a = list(range(0, len(qlt_lst)))
    qlt_url = {}
    for i in a:
        qlt_url.update({qlt_lst[i]: url_lst[i]})
    qlt1080 = ['G Drive FHD 1080p', 'Mega FHD 1080p']
    qlt720 = ['G Drive HD 720p', 'Mega HD 720p']
    qlt480 = ['G Drive SD 4880p', 'Mega SD 480p']
    sz_qlt = {}

    for m in qlt1080:
        for y in qlt_lst:
            if m in y:
                sz_qlt.update({size1080: y})
    for m in qlt720:
        for y in qlt_lst:
            if m in y:
                sz_qlt.update({size720: y})
    for m in qlt480:
        for y in qlt_lst:
            if m in y:
                sz_qlt.update({size480: y})
    sz_url = {};

    for m in qlt1080:
        for y in qlt_url:
            if m in y:
                sz_url.update({size1080: qlt_url[m]})
    for m in qlt720:
        for y in qlt_url:
            if m in y:
                sz_url.update({size720: qlt_url[m]})
    for m in qlt480:
        for y in qlt_url:
            if m in y:
                sz_url.update({size480: qlt_url[m]})
    indices = [v for i, v in enumerate(sz_lst) if v < float(2)]
    max_sz = max(indices)
    qlt_kw = ['G Drive ', 'Mega ']
    max_qlt = sz_qlt[max_sz]
    for p in qlt_kw:
        if p in max_qlt:
            max_qlt = max_qlt.replace(p, "")
    Trnl.sh2.update('H2',max_qlt)
    max_lk = sz_url[max_sz]
    gdrv_req = requests.get(max_lk)
    gdrv_req.encoding = gdrv_req.apparent_encoding
    gdrv_html = gdrv_req.text
    soup = BeautifulSoup(gdrv_html, 'html.parser')
    href_lst = []
    for a in soup.find_all('a', href=True):
        href_lst.append(a['href'])
    startswith_lst = ['https://drive.google.com/file/d/', 'https://mega.nz/file/']
    dllk_lst = []
    for h in href_lst:
        for k in startswith_lst:
            if k in h:
                dllk_lst.append([x for x in href_lst if x.startswith(k)][0])
    Trnl.sh2.update('Q2', dllk_lst)
    dllk = dllk_lst[0]
    return dllk
