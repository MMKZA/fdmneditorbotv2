import requests
from bs4 import BeautifulSoup
import re
from trnl import Trnl
from lxml import html
from translation import Translation
from helper_funcs.fdmn_frame import fdmn_frame
import time

def imdb_info(imdb_id):
    typ = Trnl.sh2.acell('P3').value
    imdb_url = 'https://www.imdb.com/title/' + str(imdb_id)
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    imdb_req = requests.get(imdb_url,headers=headers)
    time.sleep(5)
    imdb_req.encoding = imdb_req.apparent_encoding
    imdb_html = imdb_req.text
    imdb_soup = BeautifulSoup(imdb_html, 'html.parser')
    if 'Movie' in typ:
        vcap = '⁉️'
        for x in imdb_soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-80d4314-0.fjPRnj > div.sc-80d4314-1.fbQftq > h1'):
            vcap = x.text
        year = '⁉️'
        for x in imdb_soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-80d4314-0.fjPRnj > div.sc-80d4314-1.fbQftq > div > ul > li:nth-child(1) > span'):
            year = x.text
        rntm = '⁉️'
        for x in imdb_soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-80d4314-0.fjPRnj > div.sc-80d4314-1.fbQftq > div > ul > li:nth-child(3)'):
            rntm = x.text
        if rntm == '⁉️':
            for x in imdb_soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-80d4314-0.fjPRnj > div.sc-80d4314-1.fbQftq > div > ul > li:nth-child(2)'):
                rntm = x.text
        gnr_lst = []
        for x in imdb_soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-2a827f80-2.kqTacj > div.sc-2a827f80-10.fVYbpg > div.sc-2a827f80-4.bWdgcV > div.sc-16ede01-8.hXeKyz.sc-2a827f80-11.kSXeJ > div > div.ipc-chip-list__scroller > a > span'):
            gnr_lst.append(x.text)
        if len(gnr_lst) == 0:
            for x in imdb_soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-2a827f80-6.jXSdID > div.sc-2a827f80-10.fVYbpg > div.sc-2a827f80-8.indUzh > div.sc-16ede01-9.bbiYSi.sc-2a827f80-11.kSXeJ > div.ipc-chip-list--baseAlt.ipc-chip-list.sc-16ede01-5.ggbGKe > div.ipc-chip-list__scroller > a'):
                gnr_lst.append(x.text)
        mv_gnr = ", ".join(g for g in gnr_lst)
    if 'Series' in typ:
        vcap = '⁉️'
        for x in imdb_soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-80d4314-0.fjPRnj > div.sc-80d4314-1.fbQftq > h1'):
            vcap = x.text
        year = '⁉️'
        for x in imdb_soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-80d4314-0.fjPRnj > div.sc-80d4314-1.fbQftq > div > ul > li:nth-child(2) > span'):
            year = x.text
        rntm = '⁉️'
        for x in imdb_soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-80d4314-0.fjPRnj > div.sc-80d4314-1.fbQftq > div > ul > li:nth-child(4)'):
            rntm = x.text
        gnr_lst = []
        for x in imdb_soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-2a827f80-2.kqTacj > div.sc-2a827f80-10.fVYbpg > div.sc-2a827f80-4.bWdgcV > div.sc-16ede01-8.hXeKyz.sc-2a827f80-11.kSXeJ > div > div.ipc-chip-list__scroller > a'):
            gnr_lst.append(x.text)
        mv_gnr = ", ".join(g for g in gnr_lst)
    ctry_txt = []
    for x in imdb_soup.findAll('a',{'class':'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'}):
        ctry_txt.append(x.text)
    ctry_all = []
    for c in Translation.ctry_lst:
        for t in ctry_txt:
            if c == t:
                ctry_all.append(c)
    vcap_hsh = '⁉️'
    if vcap != '⁉️' or vcap != '' or year != '⁉️' or year != '':
        vcap_hsh = ''.join(e for e in vcap+year if e.isalnum())
    ctry = ", ".join(g for g in ctry_all)
    web_url = Trnl.sh2.acell('M2').value
    credit_lst = {'channelmyanmar':'Channel Myanmar','goldchannel':'Gold Channel Movies','burmesesubtitles':'Burmese Subtitles','shweflix':'ShweFlix'}
    for c in credit_lst:
        if c in web_url:
            credit = str(credit_lst[c])
    imdb_rt = ''
    imdb_vt = ''
    imdb = ''
    imdb_req = requests.get(imdb_url,headers={'Connection':'close'})
    imdb_req.encoding = imdb_req.apparent_encoding
    imdb_html = imdb_req.text
    imdb_soup = BeautifulSoup(imdb_html, 'html.parser')
    for i in imdb_soup.select(
            '#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-80d4314-0.fjPRnj > div.sc-db8c1937-0.eGmDjE.sc-80d4314-3.iBtAhY > div > div:nth-child(1) > a > div > div > div.sc-7ab21ed2-0.fAePGh > div.sc-7ab21ed2-2.kYEdvH > span.sc-7ab21ed2-1.jGRxWM'):
        imdb_rt = i.text
    for i in imdb_soup.select(
            '#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-ca85a21c-0.efoFqn > section > div:nth-child(4) > section > section > div.sc-80d4314-0.fjPRnj > div.sc-db8c1937-0.eGmDjE.sc-80d4314-3.iBtAhY > div > div:nth-child(1) > a > div > div > div.sc-7ab21ed2-0.fAePGh > div.sc-7ab21ed2-3.dPVcnq'):
        imdb_vt = i.text
    imdb = imdb_rt + '/10 (' + imdb_vt + ' Votes)'
    if imdb_rt == '':
        imdb = '⁉️'
    imdb_hrf = []
    for x in imdb_soup.find_all('a', href=True):
        imdb_hrf.append(x['href'])
    for i in imdb_hrf:
        if '/?ref_=tt_ov_i' in i:
            imdb2_url = 'https://www.imdb.com' + i
    imdb2_req = requests.get(imdb2_url)
    imdb2_req.encoding = imdb2_req.apparent_encoding
    imdb2_html = imdb2_req.text
    imdb2_soup = BeautifulSoup(imdb2_html, 'html.parser')
    imdb2_hrf = []
    for all in imdb2_soup.find_all('meta'):
        imdb2_hrf.append(all)
    imdb2 = "".join([str(lk) for lk in imdb2_hrf])
    phto_url = re.search("(?P<url>https?://[^\s]+)", imdb2).group("url").replace('"', '')
    fdmn_frame(phto_url)
    if Trnl.sh2.acell('M4').value == '⁉️':
        Trnl.sh2.update('M4', rntm)
    if Trnl.sh2.acell('M3').value == '⁉️':
        Trnl.sh2.update('M3', mv_gnr)
    if year != '⁉️' or year != '':
        Trnl.sh2.update('M5', year)
    Trnl.sh2.update('M6', ctry)
    Trnl.sh2.update('C2', phto_url)
    if vcap != '⁉️' or vcap != '':
        Trnl.sh2.update('D2', vcap)
    Trnl.sh2.update('M8', imdb)
    Trnl.sh2.update('F2', credit)
    Trnl.sh2.update('C4',phto_url)
    if vcap_hsh = '⁉️':
        Trnl.sh2.update('E2', vcap_hsh)
