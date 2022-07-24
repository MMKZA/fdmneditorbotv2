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
    szs_lst = []
    for a in soup.find_all('span', {'class': 'c'}):
        szs_lst.append(a.text)
    sz_lst = list(range(0, len(szs_lst)))
    a = list(range(1, len(szs_lst)))
    chss_lst = list(range(0, len(szs_lst)))
    for i in chss_lst:
        chss_lst[i] = url_lst[i] + " | " + qlt_lst[i] + " | " + szs_lst[i]
    cnmm_lst = list(filter(lambda x: "https://yoteshinportal.cc/" in x, chss_lst))
    gb_lst = ['GB', 'Gb', 'gb' 'gB']
    mb_lst = ['MB', 'Mb', 'mb' 'mB']
    sz_qlt = {}
    sz_lks = {}
    for k in qlt_lst:
        if "1080" in k:
            kwd_1080 = list(filter(lambda x: "1080" in x, qlt_lst))[0]
            cnmm_1080 = list(filter(lambda x: kwd_1080 in x, cnmm_lst))
            spl_1080 = " | " + kwd_1080 + " | "
            lk_1080 = re.search("(?P<url>https?://[^\s]+)", cnmm_1080[0]).group("url")
            szstr_1080 = (cnmm_1080[0].split(spl_1080))[1]
            szspl_1080 = re.findall('(\d+|[A-Za-z]+)', szstr_1080)
            szunt_1080 = szspl_1080[len(szspl_1080) - 1]
            for a in gb_lst:
                if szunt_1080 in a:
                    sz_1080 = "{:.2f}".format(float(szstr_1080.replace(szunt_1080, "").strip()))
            for a in mb_lst:
                if szunt_1080 in a:
                    sz_1080 = "{:.2f}".format(float(szstr_1080.replace(szunt_1080, "").strip()) / 1024)
            sz_qlt.update({sz_1080: k})
            sz_lks.update({sz_1080: lk_1080})

    for k in qlt_lst:
        if "720" in k:
            kwd_720 = list(filter(lambda x: "720" in x, qlt_lst))[0]
            cnmm_720 = list(filter(lambda x: kwd_720 in x, cnmm_lst))
            spl_720 = " | " + kwd_720 + " | "
            lk_720 = re.search("(?P<url>https?://[^\s]+)", cnmm_720[0]).group("url")
            szstr_720 = (cnmm_720[0].split(spl_720))[1]
            szspl_720 = re.findall('(\d+|[A-Za-z]+)', szstr_720)
            szunt_720 = szspl_720[len(szspl_720) - 1]
            for a in gb_lst:
                if szunt_720 in a:
                    sz_720 = "{:.2f}".format(float((cnmm_720[0].split(spl_720))[1].replace(szunt_720, "").strip()))
            for a in mb_lst:
                if szunt_720 in a:
                    sz_720 = "{:.2f}".format(
                        float((cnmm_720[0].split(spl_720))[1].replace(szunt_720, "").strip()) / 1024)
            sz_qlt.update({sz_720: k})
            sz_lks.update({sz_720: lk_720})

    for k in qlt_lst:
        if "480" in k:
            kwd_480 = list(filter(lambda x: "480" in x, qlt_lst))[0]
            cnmm_480 = list(filter(lambda x: kwd_480 in x, cnmm_lst))
            spl_480 = " | " + kwd_480 + " | "
            lk_480 = re.search("(?P<url>https?://[^\s]+)", cnmm_480[0]).group("url")
            szstr_480 = (cnmm_480[0].split(spl_480))[1]
            szspl_480 = re.findall('(\d+|[A-Za-z]+)', szstr_480)
            szunt_480 = szspl_480[len(szspl_480) - 1]
            for a in gb_lst:
                if szunt_480 in a:
                    sz_480 = "{:.2f}".format(float(szstr_480.replace(szunt_480, "").strip()))
            for a in mb_lst:
                if szunt_480 in a:
                    sz_480 = "{:.2f}".format(float(szstr_480.replace(szunt_480, "").strip()) / 1024)
            sz_qlt.update({sz_480: k})
            sz_lks.update({sz_480: lk_480})

    arr = list(range(1, len(szs_lst)))
    a = list(range(1, len(szs_lst)))
    for x in gb_lst:
        for i in a:
            if x in szs_lst[i]:
                arr[i - 1] = float("{:.2f}".format(float(szs_lst[i].replace(x, "").strip())))
    for x in mb_lst:
        for i in a:
            if x in szs_lst[i]:
                arr[i - 1] = float("{:.2f}".format(float(szs_lst[i].replace(x, "").strip()) / 1024))
    indices = [v for i, v in enumerate(arr) if v < float(2)]
    print(sz_1080)
    max_sz = "{:.2f}".format(max(indices))
    max_qlt = sz_qlt[max_sz]
    Trnl.sh1.update('H3', max_qlt)
    ytsn_lk = sz_lks[max_sz]
    return ytsn_lk
