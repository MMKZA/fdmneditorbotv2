import requests
from bs4 import BeautifulSoup
import re
from trnl import Trnl
from lxml import html

import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger('chardet.universaldetector').setLevel(logging.INFO)

def shweflix(web_url):
    web_req = requests.get(web_url)
    tree = html.fromstring(web_req.content)
    web_req.encoding = web_req.apparent_encoding
    web_html = web_req.text
    soup = BeautifulSoup(web_html, 'html.parser')
    urls_lsts = []
    for a in soup.findAll('a',href=True):
        if 'https://shweflix.org/dl/?key=' in str(a):
            urls_lsts.append(a['href'])
    urls_lst = list(range(0,int((len(urls_lsts))/3)))
    for i in urls_lst:
        urls_lst[i] = urls_lsts[i+2*int((len(urls_lsts))/3)]
    txts_lst = re.findall(r'<span>(.*?)</span>', web_req.text)
    gb_lst = ['GB', 'Gb', 'gb' 'gB']
    mb_lst = ['MB', 'Mb', 'mb' 'mB']
    txt_lst = []
    for gb in gb_lst:
        for mb in mb_lst:
            for txt in txts_lst:
                if gb in txt or mb in txt:
                    txt_lst.append(txt)
    txt_lst = list(dict.fromkeys(txt_lst))
    qlt_lst = []
    sz_lst = []
    for t in txt_lst:
        qlt_lst.append(t.split('[')[0].strip())
        sz_lst.append(t.split('[')[-1].replace(']',''))
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
    url_lst = []
    for url in urls_lst:
        web_req = requests.get(url)
        url_lst.append(re.findall('https://[a-zA-Z]+\.gdtot\.[a-zA-Z]+/file/[0-9]+',web_req.text)[0])
        del web_req
    all_lst = list(range(0,len(url_lst)))
    for i in all_lst:
        all_lst[i] = '{} | {} | {} GB'.format(url_lst[i],qlt_lst[i],szgb_lst[i])
    return all_lst

