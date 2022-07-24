import requests
from bs4 import BeautifulSoup
from trnl import Trnl

def func_scpt(script_url):
    req = requests.get(script_url)
    # override encoding by real educated guess as provided by chardet
    req.encoding = req.apparent_encoding
    # access the data
    html_text = req.text
    soup = BeautifulSoup(html_text, 'html.parser')
    wscpt = soup.prettify()
    sscpt = soup.get_text()
    if "goldchannel" in script_url:
        if 'tvshows' in script_url:
            start1 = 'Synopsis  '
            end1 = '   Original title'
        if 'tvshows' not in script_url:
            start1 = 'Synopsis  '
            end1 = '    Original title'
        start2 = 'image" src="'
        end2 = '.jpg'
        vcap = sscpt.split('      ', 1)[0]
        vtext = (sscpt.split(start1))[1].split(end1)[0]
    elif "channelmyanmar" in script_url:
        if 'tvshows' in script_url:
            start1 = 'Synopsis of '
            end1 = 'Translat'
        if 'tvshows' not in script_url:
            start1 = 'Complete cast'
            end1 = 'Download Nulled Scripts and Plugins'
        start2 = 'image" src="'
        end2 = '.jpg'
        vcap = sscpt.split('\n', 1)[0]
        vtext = (sscpt.split(start1))[1].split(end1)[0]
        del_vtext = 'Your browser does not support the video tag.  '
        if del_vtext in vtext:
            vtext = vtext.replace(del_vtext, '')
    vlink = (wscpt.split(start2))[1].split(end2)[0] + '.jpg'
    phto_splt = vlink.split('/')
    if 'tmdb' in vlink:
        if "channelmyanmar" in script_url:
            phto_cd = phto_splt[-1]
            phto_url = 'https://image.tmdb.org/t/p/original/' + phto_cd
    elif 'tmdb' not in vlink:
        if "goldchannel" in script_url:
            phto_cd = phto_splt[-1].replace('-200x300', '')
            phto_url = 'https://image.tmdb.org/t/p/original/' + phto_cd
        elif "channelmyanmar" in script_url:
            start3 = 'https://www.imdb.com/title/t'
            end3 = '/" target="_blank">'
            start4 = '/mediaviewer/'
            end4 = '/?ref_=tt_ov_i'
            start5 = 'https://'
            end5 = '.jpg'
            if start3 in wscpt:
                imdb_cd = (wscpt.split(start3))[1].split(end3)[0]
                imdb_url = start3 + imdb_cd
                imdb_req = requests.get(imdb_url)
                imdb_req.encoding = imdb_req.apparent_encoding
                imdb_html = imdb_req.text
                imdb_soup = BeautifulSoup(imdb_html, 'html.parser')
                imdb_wscpt = imdb_soup.prettify()
                imdb2_cd = (imdb_wscpt.split(start4))[1].split(end4)[0]
                imdb2_url = imdb_url + '/mediaviewer/' + imdb2_cd
                imdb2_req = requests.get(imdb2_url)
                imdb2_req.encoding = imdb2_req.apparent_encoding
                imdb2_html = imdb2_req.text
                imdb2_soup = BeautifulSoup(imdb2_html, 'html.parser')
                imdb2_wscpt = imdb2_soup.prettify()
                imdb3_cd = (imdb2_wscpt.split(start5))[1].split(end5)[0]
                phto_url = start5 + imdb3_cd + end5
            elif start3 not in wscpt:
                phto_url = vlink
    else:
        phto_url = vlink
    vd_qlt = Trnl.sh1.acell('H3').value
    Trnl.sh1.update('A2', vcap + " | " + vd_qlt + "\n\nဇာတ်ညွှန်း 📜\n\n" + vtext)
    Trnl.sh1.update('C2', phto_url)
    Trnl.sh1.update('D2', vcap)
    vcap_hsh = ''.join(e for e in vcap if e.isalnum())
    if 'ChannelMyanmar' in vcap_hsh:
        vcap_hsh = vcap_hsh.replace('ChannelMyanmar', '')
    elif 'GoldChannelMovies' in vcap_hsh:
        vcap_hsh = vcap_hsh.replace('GoldChannelMovies', '')
    else:
        vcap_hsh = vcap_hsh
    Trnl.sh1.update('E2', vcap_hsh)
    if "goldchannel" in script_url:
        credit = 'Gold Channel Movies'
    elif "channelmyanmar" in script_url:
        credit = 'Channel Myanmar'
    Trnl.sh1.update('F2', credit)
    msg_whl = phto_url + "\n\n" + vcap + "\n\nဇာတ်ညွှန်း 📜\n\n" + vtext
    msg_trm = msg_whl[0:4095]
    Trnl.sh1.update('O3', msg_trm)
