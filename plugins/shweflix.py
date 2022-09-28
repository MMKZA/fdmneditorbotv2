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
    txt_lst = re.findall('<span>[0-9]+p \[[0-9]+ [a-zA-Z]+\]</span>',web_req.text)
    for txt in txt_lst:
        txt_lst[txt_lst.index(txt)] = re.findall('[0-9]+p \[[0-9]+ [a-zA-Z]+\]',txt)[0]
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
    url_lst = []
    for url in urls_lst:
        web_req = requests.get(url)
        web_req.encoding = web_req.apparent_encoding
        web_html = web_req.text
        soup = BeautifulSoup(web_html, 'html.parser')
        hrf_lst = []
        for s in soup.find_all('a', href=True):
            hrf_lst.append(s)
        for h in hrf_lst:
            if 'gdtot' in str(h):
                url_lst.append(h['href'])
    all_lst = list(range(0,len(url_lst)))
    for i in all_lst:
        all_lst[i] = '{} | {} | {} GB'.format(url_lst[i],qlt_lst[i],szgb_lst[i])
    return all_lst

