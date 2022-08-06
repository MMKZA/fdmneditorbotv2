import requests
from bs4 import BeautifulSoup
import re
from trnl import Trnl
import json
from json2html import *

def blc(web_url):
    if "burmalinkchannel" in web_url:
        web_url = 'https://api.burmalinkchannel.com/moviedetail/' + web_url.split('/')[-1]
    web_req = requests.get(web_url)
    web_req.encoding = web_req.apparent_encoding
    web_html = web_req.text
    soup = BeautifulSoup(web_html, 'html.parser')
    jsn1 = json.loads(web_html)
    html = json2html.convert(json=jsn1)
    soup = BeautifulSoup(html, 'html.parser')
    # DOWNLOAD_LINK
    td_lst = []
    for d in soup.find("th", text="download").find_next_sibling("td").find_all("tr"):
        td_lst.append(d.find_all("td"))
    index = list(range(0, len(td_lst)))
    all_lst = []
    for i in index:
        for u in td_lst[i]:
            all_lst.append(u.text)
    sz_lst = []
    url_lst = []
    qlt_lst = []
    index = list(range(1, len(td_lst)))
    for i in index:
        # url_lst.append('{} | {} | {} | {}'.format(all_lst[5*i-4],all_lst[5*i-3],all_lst[5*i-2],all_lst[5*i-1]))
        sz_lst.append(all_lst[5 * i - 2])
        url_lst.append(all_lst[5 * i - 4])
        qlt_lst.append(all_lst[5 * i - 3])
    try:
        # GB_UNIT_CONVERSION
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
        # PARING_ALL_LIST
        all_lst = list(range(0, len(szgb_lst)))
        for i in all_lst:
            all_lst[i] = ("{} | {} | {}".format(url_lst[i], qlt_lst[i], str(szgb_lst[i]) + "GB"))
        # FINDING_MAX_SIZE
        indices = [v for i, v in enumerate(szgb_lst) if v < 2]
        max_sz = float("{:.2f}".format(max(indices)))
        # MAX_LIST
        max_lst = list(filter(lambda x: str(max_sz) + "GB" in x, all_lst))
        # FILTER_LIST
        blc_lst = []
        kwd_st = ['https://drive.google.com/', 'https://mega.nz/file/']
        for k in kwd_st:
            for m in max_lst:
                if k in m:
                    blc_lst.append(m.split("|", 3)[0])
        prr_blc = blc_lst[0]
        max_lk = prr_blc.split("|", 3)[0]
        # MAX_QUALITY
        qlt_kwd = []
        max_qlt = ""
        for k in qlt_lst:
            if "" != k:
                qlt_kwd.append(k)
        for m in max_lst:
            for q in qlt_kwd:
                if q in m:
                    max_qlt = m.split("|", 3)[1]
        if max_qlt == "":
            max_qlt = "HD"
        avlb_lk = '\n'.join([str(lk) for lk in all_lst])
        Trnl.sh2.update('Q2', avlb_lk)
        Trnl.sh2.update('H2', max_qlt)
        ytsn_lk = max_lk
    except:
        all_lst = list(range(0, len(sz_lst)))
        for i in all_lst:
            all_lst[i] = ("{} | {} | {}".format(url_lst[i], qlt_lst[i], str(sz_lst[i])))
            ytsn_lk = 'အခက်အခဲဖြစ်ပေါ်နေလို့ Manual ရွေးပါ\n' + "\n".join([str(lk) for lk in all_lst])
    return ytsn_lk
