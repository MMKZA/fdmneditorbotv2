import pyrogram
import requests
from bs4 import BeautifulSoup
import re
def series(web_url):
    web_req = requests.get(web_url)
    # override encoding by real educated guess as provided by chardet
    web_req.encoding = web_req.apparent_encoding
    # access the data
    web_html = web_req.text
    soup = BeautifulSoup(web_html, 'html.parser')
    if "goldchannel" in web_url:
        hrf_lst = []
        for a in soup.select('#seasons > div > div.se-a', href=True):
            hrf_lst.append(a)
        hrf_str = "\n".join([str(lk) for lk in hrf_lst]).split('"')
        url_lst = []
        for h in hrf_str:
            if 'https://goldchannel.net/episodes/' in h:
                url_lst.append(h)
        dllk_lst = []
        for u in url_lst:
            dllk = gldchnl(u)
            dllk_lst.append(dllk)
        avlb_lst = '\n'.join([d for d in dllk_lst])
        return avlb_lst
    if "channelmyanmar" in web_url:
        url_lst = []
        for a in soup.find_all('a', href=True):
            url_lst.append(a['href'])
        ytsn_lst = []
        mega_lst = []
        for l in url_lst:
            if 'yoteshinportal.cc' in l:
                ytsn_lst.append(l)
            elif 'mega.nz' in l:
                mega_lst.append(l)

        ytsn_1080 = []
        ytsn_720 = []
        ytsn_hd = []
        mega_1080 = []
        mega_720 = []
        mega_hd = []

        for y in ytsn_lst:
            if "1080" in y:
                ytsn_1080.append(y)
                if len(mega_lst) == len(ytsn_lst):
                    mega_1080.append(mega_lst[ytsn_lst.index(y)])
            elif "720" in y:
                ytsn_720.append(y)
                if len(mega_lst) == len(ytsn_lst):
                    mega_720.append(mega_lst[ytsn_lst.index(y)])
            else:
                ytsn_hd.append(y)
                if len(mega_lst) == len(ytsn_lst):
                    mega_hd.append(mega_lst[ytsn_lst.index(y)])

        fnl_lst = []
        if len(ytsn_1080) != 0:
            lk = ytsn_1080[len(ytsn_1080) - 1]
            web_req = requests.get(lk)
            web_html = web_req.text
            soup = BeautifulSoup(web_html, 'html.parser')
            sz1080 = soup.find('span', {'class': 'badge badge-danger mr-1'}).text
            fnl_lst.append(lk + ' | ' + sz1080)
        if len(ytsn_720) != 0:
            lk = ytsn_720[len(ytsn_720) - 1]
            web_req = requests.get(lk)
            web_html = web_req.text
            soup = BeautifulSoup(web_html, 'html.parser')
            sz720 = soup.find('span', {'class': 'badge badge-danger mr-1'}).text
            fnl_lst.append(lk + ' | ' + sz720)
        if len(ytsn_hd) != 0:
            lk = ytsn_hd[len(ytsn_hd) - 1]
            web_req = requests.get(lk)
            web_html = web_req.text
            soup = BeautifulSoup(web_html, 'html.parser')
            szhd = soup.find('span', {'class': 'badge badge-danger mr-1'}).text
            fnl_lst.append(lk + ' | ' + szhd)

        if len(mega_1080) != 0:
            lk = mega_1080[len(mega_1080) - 1]
            fnl_lst.append(lk + ' | ' + sz1080)
        if len(mega_720) != 0:
            lk = mega_720[len(mega_720) - 1]
            fnl_lst.append(lk + ' | ' + sz720)
        if len(mega_hd) != 0:
            lk = mega_hd[len(mega_hd) - 1]
            fnl_lst.append(lk + ' | ' + szhd)
        if len(ytsn_lst) != 0:
            ytsn_epsd = "Yoteshin Episodes အားလုံး👇\n" + "\n".join([str(lk) for lk in ytsn_lst])
        if len(mega_lst) != 0:
            mega_epsd = "Mega Episodes အားလုံး👇\n" + "\n".join([str(lk) for lk in mega_lst])
        last_epsd = "နောက်ဆုံးတင်ထားသော Episode👇\n" + "\n".join([str(lk) for lk in fnl_lst])
        try:
            return [ytsn_epsd, mega_epsd, last_epsd]
        except:
            return [ytsn_epsd, last_epsd]
