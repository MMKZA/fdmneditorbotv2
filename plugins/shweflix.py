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
    if "shweflix" in web_url:
        urls_lst = []
        for x in soup.select('div > div > div.wp-block-essential-blocks-advanced-tabs.alignwide > div > div > div.eb-tabs-contents > div:nth-child(3) > div > div > div > a'):
            urls_lst.append(x['href'])
        logger.info(urls_lst)
        txt_lst = []
        for x in soup.select('div > div > div.wp-block-essential-blocks-advanced-tabs.alignwide > div > div > div.eb-tabs-contents > div:nth-child(3) > div > div > div'):
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
                if 'gdtot.sbs/file/' in str(h):
                    url_lst.append(h['href'])
        logger.info(url_lst)
        all_lst = list(range(0,len(url_lst)))
        for i in all_lst:
            all_lst[i] = '{} | {} | {} GB'.format(url_lst[i],qlt_lst[i],szgb_lst[i])
        logger.info(all_lst)
        return all_lst

