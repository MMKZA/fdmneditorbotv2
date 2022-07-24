import requests
from bs4 import BeautifulSoup
import re
from trnl import Trnl

def gldchnl(gld_url):
    web_req = requests.get(gld_url)
    web_req.encoding = web_req.apparent_encoding
    web_html = web_req.text
    soup = BeautifulSoup(web_html, 'html.parser')
    urls_lst = []
    for a in soup.find_all('a', href=True):
        urls_lst.append(a['href'])
    url_lst = [x for x in urls_lst if x.startswith('https://goldchannel.net/links/')]
    sizes_lst = []
    for a in soup.find_all("strong", {"class": "quality"}):
        sizes_lst.append(a.text)
    table = ''
    for a in soup.find_all('div', {'class': 'links_table'}):
        table = a.text
    sttrm1080 = 'G Drive FHD 1080pMyanmar'
    sttrm720 = 'G Drive HD 720pMyanmar'
    sttrm480 = 'G Drive SD 480pMyanmar'
    entrmGB = ' GB'
    entrmMB = ' MB'
    sz_lst = []
    if sttrm1080 in table:
        if entrmGB in table:
            size1080 = (table.split(sttrm1080))[1].split(entrmGB)[0]
            if "Myanmar" in size1080:
                size1080 = "{:.2f}".format(float((table.split(sttrm1080))[1].split(entrmMB)[0]) / 1024)
            else:
                size1080 = "{:.2f}".format(float(size1080))
            sz_lst.append(float(size1080))
    if sttrm720 in table:
        if entrmGB in table:
            size720 = (table.split(sttrm720))[1].split(entrmGB)[0]
            if "Myanmar" in size720:
                size720 = "{:.2f}".format(float((table.split(sttrm720))[1].split(entrmMB)[0]) / 1024)
            else:
                size720 = "{:.2f}".format(float(size720))
            sz_lst.append(float(size720))
    if sttrm480 in table:
        size480 = "{:.2f}".format(float((table.split(sttrm480))[1].split(entrmMB)[0]) / 1024)
        sz_lst.append(float(size480))
    a = list(range(0, len(sizes_lst)))
    chs_lst = list(range(0, len(sizes_lst)))
    chss_lst = list(range(0, len(sizes_lst)))
    for i in a:
        chs_lst[i] = url_lst[i] + " | " + sizes_lst[i]
    for i in a:
        if "1080" in chs_lst[i]:
            chss_lst[i] = chs_lst[i] + " | " + str(size1080) + "GB"
        if "720" in chs_lst[i]:
            chss_lst[i] = chs_lst[i] + " | " + str(size720) + "GB"
        if "480" in chs_lst[i]:
            chss_lst[i] = chs_lst[i] + " | " + str(size480) + "GB"
    gdrv_1080 = ''
    gdrv_720 = ''
    gdrv_480 = ''
    gld_lk = ''
    sz_qlt = {}
    sz_lks = {}
    for a in chss_lst:
        if "G Drive FHD 1080p" in a:
            gdrv_1080 = list(filter(lambda x: "G Drive FHD 1080p" in x, chss_lst))
            lk_1080 = re.search("(?P<url>https?://[^\s]+)", gdrv_1080[0]).group("url")
            sz_qlt.update({size1080:"G Drive FHD 1080p".replace("G Drive ","")})
            sz_lks.update({size1080:lk_1080})
        if "G Drive HD 720p" in a:
            gdrv_720 = list(filter(lambda x: "G Drive HD 720p" in x, chss_lst))
            lk_720 = re.search("(?P<url>https?://[^\s]+)", gdrv_720[0]).group("url")
            sz_qlt.update({size720:"G Drive HD 720p".replace("G Drive ","")})
            sz_qlt.update({size720:lk_720})
        if "G Drive SD 480p" in a:
            gdrv_480 = list(filter(lambda x: "G Drive SD 480p" in x, chss_lst))
            lk_480 = re.search("(?P<url>https?://[^\s]+)", gdrv_480[0]).group("url")
            sz_qlt.update({size480:"G Drive SD 480p".replace("G Drive ","")})
            sz_qlt.update({size480:lk_480})
    indices = [v for i, v in enumerate(sz_lst) if v < float(2)]
    max_sz = "{:.2f}".format(max(indices))
    max_qlt = sz_qlt[max_sz]
    Trnl.sh1.update('H3', max_qlt)
    max_lk = sz_lks[max_sz]
    gld_req = requests.get(max_lk)
    gld_req.encoding = gld_req.apparent_encoding
    gld_html = gld_req.text
    soup = BeautifulSoup(gld_html, 'html.parser')
    gld_lsts = []
    for a in soup.find_all('a', href=True):
        gld_lsts.append(a['href'])
    gdrv_lk = [x for x in gld_lsts if x.startswith('https://drive.google.com/file/d/')][0]
    return gdrv_lk
