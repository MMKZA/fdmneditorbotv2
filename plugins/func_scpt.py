import requests
from bs4 import BeautifulSoup
from trnl import Trnl
import logging
import re
import json
import urllib
import datetime
from tmdbv3api import TMDb, Search, Genre
from json2html import *
from translation import Translation
from lxml import html
from channels import channels
from helper_funcs.imdb_search import google
from helper_funcs.fdmn_frame import fdmn_frame
from plugins.imdb_info import imdb_info

logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def func_scpt(script_url):
    if "burmalinkchannel" in script_url:
        if 'series' in script_url:
            script_url = 'https://api.burmalinkchannel.com/seriesdetail/' + script_url.split('/')[-1]
        if 'movies' in script_url:
            script_url = 'https://api.burmalinkchannel.com/moviedetail/' + script_url.split('/')[-1]
    req = requests.get(script_url)
    tree = html.fromstring(req.content)
    req.encoding = req.apparent_encoding
    html_text = req.text
    soup = BeautifulSoup(html_text, 'html.parser')
    wscpt = soup.prettify()
    sscpt = soup.get_text()
    tmdb = TMDb()
    tmdb.api_key = "53b9eff4684ba49f0f2225d888fd4202"
    search = Search()
    genre = Genre()
    if "shweflix" in script_url:
        vcap = ''
        try:
            for all in soup.select('div > div.entry-header > h1'):
                vcap = all.text
        except:
            pass
        if vcap == '':
            for all in soup.select('div > header > h1'):
                vcap = all.text
        year = ''
        try:
            year = re.findall(r'(\d+)', vcap)[len(re.findall(r'(\d+)', vcap)) - 1]
        except:
            pass
        title = vcap.replace('(' + year + ')', '').strip()
        rmv = ['(21+)', '{21+}', '[21+]', '(18+)', '{18+}', '[18+]']
        for r in rmv:
            if r in title:
                title = title.replace(r, '').strip()
        omdb_url = 'https://www.omdbapi.com/?t=' + urllib.parse.quote_plus(title) + '&y=' + year + '&apikey=39ecaf7'
        omdb_req = json.loads(requests.get(omdb_url).content.decode('utf8'))
        if Trnl.sh2.acell('N7').value == 'close':
            imdb_hrf = []
            for h in soup.find_all('a', href=True):
                imdb_hrf.append(h['href'])
            for h in imdb_hrf:
                if "https://www.imdb.com/title/t" in h:
                    imdb_id = h.split('/', 5)[4]
            if ('Error' not in omdb_req) and ('imdbID' in omdb_req) and (str(omdb_req['imdbID']) != 'N/A') and (imdb_id == ''):
                imdb_id = omdb_req['imdbID']
            if imdb_id == '':
                imdb_wrn = "⚠️အောက်ပါဇာတ်လမ်းအတွက် IMDB ID လိုအပ်နေပါတယ်⚠️👇\n" + script_url
                Trnl.sh2.update('L3', imdb_wrn)
                imdb_id = google('{} {} imdb'.format(title,year))[0]
        if Trnl.sh2.acell('N7').value == 'open':
                imdb_id = Trnl.sh2.acell('M7').value
        imdb_url = 'https://www.imdb.com/title/' + imdb_id
        if 'Error' in omdb_req:
            omdb_url = 'https://www.omdbapi.com/?i=' + imdb_id + '&apikey=39ecaf7'
            omdb_req = json.loads(requests.get(omdb_url).content.decode('utf8'))
        if 'Movie' in Trnl.sh2.acell('P3').value:
            results = search.movies({"query": title, "year": year})
            gnr = []
            mv_gnr = ''
            for g in soup.select(
                    'div > div.entry-content > div.imdbwp.imdbwp--movie.light > div.imdbwp__content > div.imdbwp__header > div > span:nth-child(2)'):
                gnr.append(g.text)
            if len(gnr) != 0:
                mv_gnr = gnr[0]
        if mv_gnr == '':
            try:
                mv_gnr = omdb_req['Genre']
            except:
                mv_gnr = ""
        if (mv_gnr == "") or (mv_gnr == 'N/A'):
            try:
                genres = genre.movie_list()
                gnr_lst = []
                for result in results:
                    for g in genres:
                        if g.id in result.genre_ids:
                            gnr_lst.append(g.name)
                mv_gnr = ", ".join(g for g in gnr_lst)
            except:
                mv_gnr = '⁉️️'
        if "Adult" in mv_gnr:
            Trnl.sh2.update('J2', channels.rt_chnl[0])
            Trnl.sh2.update('I2', channels.rt_chnl[1])
        elif "Animation" in mv_gnr:
            Trnl.sh2.update('J2', channels.ani_chnl[0])
            Trnl.sh2.update('I2', channels.ani_chnl[1])
        elif "Bollywood" in mv_gnr:
            Trnl.sh2.update('J2', channels.bt_chnl[0])
            Trnl.sh2.update('I2', channels.bt_chnl[1])
        else:
            Trnl.sh2.update('J2', channels.gn_chnl[0])
            Trnl.sh2.update('I2', channels.gn_chnl[1])
            Trnl.sh2.update('H3', "⚠️အောက်ကဇာတ်ကားကို v1 ဇာတ်လမ်းစုံ ကို ပို့ပါမယ်⚠️\n" + script_url)
        try:
            rntm = omdb_req['Runtime'].split(' ', 2)[0]
            rntm = "{} နာရီ : {} မိနစ်".format(*divmod(int(rntm), 60))
        except:
            rntm = ""
        if rntm == "":
            try:
                for r in soup.select(
                        'div > div.entry-content > div.imdbwp.imdbwp--movie.light > div.imdbwp__content > div.imdbwp__header > div > span:nth-child(1)'):
                    rntm = r.text
                    rntm = "{} နာရီ : {} မိနစ်".format(*divmod(int(rntm), 60))
            except:
                rntm = ""
        if rntm == "":
            rntm = '⁉️'
        ctry = ''
        try:
            ctry = omdb_req['Country']
        except:
            ctry = ''
        if ctry == '':
            ctry = '⁉️'
        if "India" in ctry:
            Trnl.sh2.update('J2', channels.bt_chnl[0])
            Trnl.sh2.update('I2', channels.bt_chnl[1])
        bd_lks = []
        bd_soup = soup.select('div > div.entry-content > p') + soup.select(
            '#post-1140 > div > div.entry-content > ul > li')
        for all in bd_soup:
            bd_lks.append(all.text)
        if len(bd_lks) != 0:
            vtext = "\n".join([str(txt) for txt in bd_lks])
        all_lks = []
        for all in soup.select('div > div.entry-content > div.imdbwp.imdbwp--movie.light > div.imdbwp__thumb > a > img'):
            try:
                all_lks.append(all['data-src'])
            except:
                all_lks.append(all['src'])
        vlink = all_lks[0]
        try:
            vlink = vlink.replace('_SX300','_FMjpg_UX1000_')
        except:
            pass
        phto_url = vlink
        credit = 'ShweFlix'
    if "burmesesubtitles" in script_url:
        try:
            for all in soup.select('#single > div.content > div.sheader > div.data > h1'):
                vcap = all.text
            try:
                year = re.findall(r'(\d+)', vcap)[len(re.findall(r'(\d+)', vcap))-1]
            except:
                for all in soup.select('#uwee > div.data > p.meta > span:nth-child(1) > a'):
                    year=all.text
            title = vcap.replace('('+year+')','').strip()
        except:
            for all in soup.select('#uwee > div.data > h1'):
                vcap = all.text
            try:
                year = re.findall(r'(\d+)', vcap)[len(re.findall(r'(\d+)', vcap))-1]
            except:
                for all in soup.select('#uwee > div.data > p.meta > span:nth-child(1) > a'):
                    year=all.text
            title = vcap.replace('('+year+')','').strip()
        rmv = ['(21+)','{21+}','[21+]','(18+)','{18+}','[18+]']
        for r in rmv:
            if r in title:
                title = title.replace(r,'').strip()
        print(title)
        print(year)
        omdb_url = 'https://www.omdbapi.com/?t=' + urllib.parse.quote_plus(title) + '&y=' + year + '&apikey=39ecaf7'
        omdb_req = json.loads(requests.get(omdb_url).content.decode('utf8'))
        if 'close' in Trnl.sh2.acell('N7').value:
            imdb_id = ''    
            imdb_hrf = []
            for h in soup.find_all('a',href=True):
                imdb_hrf.append(h['href'])
            for h in imdb_hrf:
                if "https://www.imdb.com/title/t" in h:
                    imdb_url = h
                    imdb_id = imdb_url.split('/',5)[4]
            if imdb_id == '':
                imdb_wrn = "⚠️အောက်ပါဇာတ်လမ်းအတွက် IMDB ID လိုအပ်နေပါတယ်⚠️👇\n" + script_url
                Trnl.sh2.update('L3', imdb_wrn)
                imdb_id = google('{} {} imdb'.format(title,year))[0]
            imdb_id = Trnl.sh2.update('M7',imdb_id)
        if 'open' in Trnl.sh2.acell('N7').value:
            imdb_id = Trnl.sh2.acell('M7').value
        imdb_url = 'https://www.imdb.com/title/' + str(imdb_id)
        if 'Error' in omdb_req:
            omdb_url = 'https://www.omdbapi.com/?i=' + str(imdb_id) + '&apikey=39ecaf7'
            omdb_req = json.loads(requests.get(omdb_url).content.decode('utf8'))
        if 'Movie' in Trnl.sh2.acell('P3').value:
            results = search.movies({"query": title, "year": year})
            gnr = []
            for all in soup.select('#single > div.content > div.sheader > div.data > div.sgeneros > a'):            
                gnr.append(all)
            if len(gnr) == 0:
                for all in soup.select('#uwee > div.data > p.meta > i'):            
                    gnr.append(all)
            gnr_lst = []
            for g in gnr:
                 gnr_lst.append(g.text)
            mv_gnr = ", ".join(str(g) for g in gnr_lst)
            if "Uncategorized" in mv_gnr:
                try:
                    mv_gnr = omdb_req['Genre']
                except:
                    mv_gnr = ""
                if (mv_gnr == "") or (mv_gnr == 'N/A'):
                    try:
                        genres = genre.movie_list()
                        gnr_lst = []
                        for result in results:
                            for g in genres:
                                if g.id in result.genre_ids:
                                    gnr_lst.append(g.name)
                        mv_gnr = ", ".join(g for g in gnr_lst)
                    except:
                        mv_gnr = '⁉️'
            if "Adult" in mv_gnr:
                Trnl.sh2.update('J2', '-1001750623132')
                Trnl.sh2.update('I2', 'https://t.me/c/1750623132/')
            elif "Animation" in mv_gnr:
                Trnl.sh2.update('J2', '-1001389311243')
                Trnl.sh2.update('I2', 'https://t.me/c/1389311243/')
            elif "Bollywood" in mv_gnr:
                Trnl.sh2.update('J2', '-1001718578294')
                Trnl.sh2.update('I2', 'https://t.me/c/1718578294/')
            else:
                Trnl.sh2.update('J2', '-1001785695486')
                Trnl.sh2.update('I2', 'https://t.me/c/1785695486/')
                Trnl.sh2.update('H3',"⚠️အောက်ကဇာတ်ကားကို v1 ဇာတ်လမ်းစုံ ကို ပို့ပါမယ်⚠️\n" + script_url)
        if 'Series' in Trnl.sh2.acell('P3').value:
            genres = genre.tv_list()
            try:
                mv_gnr = omdb_req['Genre']
            except:
                mv_gnr = ""
            if (mv_gnr == "") or ('N/A' == mv_gnr):
                try:
                    results = search.tv_shows({"query": title, "year": year})
                    gnr_lst = []
                    for result in results:
                        for g in genres:
                            if g.id in result.genre_ids:
                                gnr_lst.append(g.name)
                    if len(gnr_lst) > 5:
                        mv_gnr = '⁉️'
                    if len(gnr_lst) < 5:
                        mv_gnr = ", ".join(g for g in gnr_lst)
                except:
                    mv_gnr = '⁉️'
        try:
            if "India" in omdb_req['Country']:
                Trnl.sh2.update('J2', '-1001718578294')
                Trnl.sh2.update('I2', 'https://t.me/c/1718578294/')
        except:
            pass
        try:
            rntm = omdb_req['Runtime'].split(' ',2)[0]
            rntm = "{} နာရီ:{} မိနစ်".format(*divmod(int(rntm), 60))
        except:
            rntm = ""
        if rntm == "":
            try:
                for r in soup.select('#single > div.content > div.sheader > div.data > div.extra > span.runtime'):
                    rntm = r.text
                    rntm = "{} နာရီ:{} မိနစ်".format(*divmod(int(rntm), 60))
            except:
                rntm = ""
        if rntm == "":
            rntm = '⁉️'
        ctry = ''    
        for all in soup.select('#single > div.content > div.sheader > div.data > div.extra > span.country'):
            ctry = all.text
        if ctry == "":
            try:
                if 'Country' in omdb_req:
                    ctry = omdb_req['Country']
            except:
                ctry = '⁉️'
        if len(ctry) != 0:
            if "India" in ctry:
                Trnl.sh2.update('J2', '-1001718578294')
                Trnl.sh2.update('I2', 'https://t.me/c/1718578294/')
        if 'Country' in omdb_req:
            if len(omdb_req['Country']) != 0:
                if "India" in omdb_req['Country']:
                    Trnl.sh2.update('J2', '-1001718578294')
                    Trnl.sh2.update('I2', 'https://t.me/c/1718578294/')
        bd_lks = []
        bd_soup = soup.select('#info > div.wp-content')
        for all in bd_soup:
            bd_lks.append(all.text)
        if len(bd_lks) == 0:
            bd_soup = soup.select('#cap1 > p')
            for all in bd_soup:
                bd_lks.append(all.text)
        if len(bd_lks) !=0:
            vtext = "\n".join([str(txt) for txt in bd_lks])
        else:
            if 'tvshows' in script_url:
                start1 = 'Synopsis of '
                end1 = 'Translat'
            if 'tvshows' not in script_url:
                start1 = 'Complete cast'
                end1 = 'Download Nulled Scripts and Plugins'
            vtext = (sscpt.split(start1))[1].split(end1)[0]
            del_vtext = 'Your browser does not support the video tag.  '
            if del_vtext in vtext:
                vtext = vtext.replace(del_vtext, '')
        vcap = vcap
        all_lks = []
        for all in soup.select('#single > div.content > div.sheader > div.poster > img'):
            all_lks.append(all['src'])
        if len(all_lks) == 0:
            for all in soup.select('#uwee > div.imagen > div > img'):
                all_lks.append(all['src'])
        print(all_lks)
        vlink = all_lks[0]
        phto_splt = vlink.split('/')
        credit = 'Burmese Subtitles'
    if "burmalinkchannel" in script_url:
        jsn1 = json.loads(html_text)
        html_blc = json2html.convert(json=jsn1)
        soup = BeautifulSoup(html_blc, 'html.parser')
        # TITLE
        nm_td = []
        nm_lst = []
        for d in soup.find_all("th", text="name"):
            nm_td.append(d.find_next_sibling("td"))
        for n in nm_td:
            if str(n) != 'None':
                nm_lst.append(n.text)
        vcap = nm_lst[-2]
        # YEAR
        year = soup.find("th", text="reYear").find_next_sibling("td").text
        # OMDB
        omdb_url = 'https://www.omdbapi.com/?t=' + urllib.parse.quote_plus(vcap) + '&y=' + year + '&apikey=39ecaf7'
        omdb_req = json.loads(requests.get(omdb_url).content.decode('utf8'))
        # TMDB
        if 'Movie' in Trnl.sh2.acell('P3').value:
            results = search.movies({"query": vcap, "year": year})
            genres = genre.movie_list()
        if 'Series' in Trnl.sh2.acell('P3').value:
            results = search.tv_shows({"query": vcap, "year": year})
            genres = genre.tv_list()
        # SCRIPT
        vtext = soup.find("th", text="description").find_next_sibling("td").text
        # RUNTIME
        try:
            rntm = soup.find("th", text="duration").find_next_sibling("td").text
            rntm = "{} နာရီ : {} မိနစ်".format(*divmod(int(rntm), 60))
        except:
            rntm = ""
        if rntm == "":
            try:
                rntm = omdb_req['Runtime'].split(' ', 2)[0]
                rntm = "{} နာရီ : {} မိနစ်".format(*divmod(int(rntm), 60))
            except:
                rntm = '⁉️'
        # GENRE
        try:
            if 'Genre' in omdb_req:
                mv_gnr = omdb_req['Genre']
        except:
            mv_gnr = ""
        if mv_gnr == "":
            try:
                gnr_lst = []
                for s in soup.find("th", text="genre").find_next_sibling("td").find_all("li"):
                    gnr_lst.append(s.text)
                mv_gnr = ", ".join(g for g in gnr_lst)
            except:
                mv_gnr = ""
        if mv_gnr == "":
            try:
                gnr_lst = []
                for result in results:
                    for g in genres:
                        if g.id in result.genre_ids:
                            gnr_lst.append(g.name)
                mv_gnr = ", ".join(g for g in gnr_lst)
            except:
                mv_gnr = "⁉️"
        # GENRE_RELATED
        if "Adult" in mv_gnr:
            Trnl.sh2.update('J2', channels.rt_chnl[0])
            Trnl.sh2.update('I2', channels.rt_chnl[1])
        elif "Animation" in mv_gnr:
            Trnl.sh2.update('J2', channels.ani_chnl[0])
            Trnl.sh2.update('I2', channels.ani_chnl[1])
        elif "Bollywood" in mv_gnr:
            Trnl.sh2.update('J2', channels.bt_chnl[0])
            Trnl.sh2.update('I2', channels.bt_chnl[1])
        else:
            Trnl.sh2.update('J2', channels.gn_chnl[0])
            Trnl.sh2.update('I2', channels.gn_chnl[1])
            Trnl.sh2.update('H3', "⚠️အောက်ကဇာတ်ကားကို v1 ဇာတ်လမ်းစုံ ကို ပို့ပါမယ်⚠️\n" + script_url)
        # COUNTRY
        ctry = soup.find("th", text="reCountry").find_next_sibling("td").text
        # COUNTRY_RELATED
        if len(ctry) != 0:
            if "India" in ctry:
                Trnl.sh2.update('J2', channels.bt_chnl[0])
                Trnl.sh2.update('I2', channels.bt_chnl[1])
        if 'Country' in omdb_req:
            if len(omdb_req['Country']) != 0:
                if "India" in omdb_req['Country']:
                    Trnl.sh2.update('J2', channels.bt_chnl[0])
                    Trnl.sh2.update('I2', channels.bt_chnl[1])
        # POSTER
        try:
            phto_url = omdb_req["Poster"].replace('_SX300', '_FMjpg_UX1000_')
        except:
            phto_url = ""
        if (phto_url == "") or ('N/A' in phto_url):
            try:
                for result in results:
                    phto_url = 'https://image.tmdb.org/t/p/original' + result.poster_path
            except:
                phto_url = ""
        if phto_url == "":
            try:
                imdb_req = requests.get(imdb_url)
                imdb_req.encoding = imdb_req.apparent_encoding
                imdb_html = imdb_req.text
                imdb_soup = BeautifulSoup(imdb_html, 'html.parser')
                imdb_hrf = []
                for all in imdb_soup.find_all('a', href=True):
                    imdb_hrf.append(all['href'])
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
            except:
                phto_url = vlink
        # CREDIT
        credit = 'Burma Link Channel'
    if "goldchannel" in script_url:
        vcap = ''
        for all in soup.select('#single > div.content.right > div.sheader > div.data > h1'):
            vcap = all.text
        year = ''
        for all in soup.select('#single > div.content.right > div.sheader > div.data > div.extra > span.date'):
            rls_date = datetime.datetime.strptime(all.text, "%b. %d, %Y")
            year = rls_date.year
        omdb_url = 'https://www.omdbapi.com/?t=' + urllib.parse.quote_plus(vcap) + '&y=' + str(year) + '&apikey=39ecaf7'
        omdb_req = json.loads(requests.get(omdb_url).content.decode('utf8'))
        if Trnl.sh2.acell('N7').value == 'close':
            imdb_id = ''
            if ('Error' not in omdb_req) and ('imdbID' in omdb_req) and (str(omdb_req['imdbID']) != 'N/A') and (imdb_id == ''):
                imdb_id = omdb_req['imdbID']
            if imdb_id == '':
                imdb_wrn = "⚠️အောက်ပါဇာတ်လမ်းအတွက် IMDB ID လိုအပ်နေပါတယ်⚠️👇\n" + script_url
                Trnl.sh2.update('L3', imdb_wrn)
                imdb_id = google('{} {} imdb'.format(title,year))[0]
        if Trnl.sh2.acell('N7').value == 'open':
            imdb_id = Trnl.sh2.acell('M7').value
        imdb_url = 'https://www.imdb.com/title/' + imdb_id
        if 'Error' in omdb_req:
            omdb_url = 'https://www.omdbapi.com/?i=' + imdb_id + '&apikey=39ecaf7'
            omdb_req = json.loads(requests.get(omdb_url).content.decode('utf8'))
        if 'Movie' in Trnl.sh2.acell('P3').value:
            results = search.movies({"query": vcap, "year": year})
            genres = genre.movie_list()
        if 'Series' in Trnl.sh2.acell('P3').value:
            results = search.tv_shows({"query": vcap, "year": year})
            genres = genre.tv_list()
        ctry = ''
        for all in soup.select('#single > div.content.right > div.sheader > div.data > div.extra > span.country'):
            ctry = all.text
        if ctry == '':
            ctry = '⁉️️'
        mv_gnr = ""
        try:
            if 'Genre' in omdb_req:
                mv_gnr = omdb_req['Genre']
        except:
            mv_gnr = ""
        if mv_gnr == "":
            try:
                for all in soup.select('#single > div.content.right > div.sheader > div.data > div.sgeneros'):
                    mv_gnr = re.sub(r"(\w)([A-Z])", r"\1, \2", all.text)
            except:
                mv_gnr = ""
        if mv_gnr == "":
            try:
                gnr_lst = []
                for result in results:
                    for g in genres:
                        if g.id in result.genre_ids:
                            gnr_lst.append(g.name)
                mv_gnr = ", ".join(g for g in gnr_lst)
            except:
                mv_gnr = ""
        if mv_gnr == "":
            mv_gnr = "⁉️️"
        rntm = ""
        try:
            if 'tvshows' in script_url:
                for all in soup.select('#info > div:nth-child(9) > span'):
                    rntm = all.text.split(' ', 2)[0]
                    rntm = "{} နာရီ : {} မိနစ်".format(*divmod(int(rntm), 60))
            if 'movies' in script_url:
                for all in soup.select(
                        '#single > div.content.right > div.sheader > div.data > div.extra > span.runtime'):
                    rntm = all.text.split(' ', 2)[0]
                    rntm = "{} နာရီ : {} မိနစ်".format(*divmod(int(rntm), 60))
        except:
            rntm = ""
        if rntm == "":
            try:
                rntm = omdb_req['Runtime'].split(' ', 2)[0]
                rntm = "{} နာရီ : {} မိနစ်".format(*divmod(int(rntm), 60))
            except:
                rntm = ""
        if rntm == "":
            rntm = '⁉️️'
        chck_rtd = ''
        for x in soup.select('#single > div.content.right > div.sheader > div.data > div.extra > span.CR.rated'):
            chck_rtd = x.text
        if len(chck_rtd) == 0:
            try:
                for y in soup.select(
                        '#single > div.content.right > div.sheader > div.data > div.extra > span.CNot.Rated.rated'):
                    chck_rtd = y.text
            except:
                chck_rtd = 'Not Rated'
        Trnl.sh2.update('J2', channels.gn_chnl[0])
        Trnl.sh2.update('I2', channels.gn_chnl[1])
        Trnl.sh2.update('H3', "⚠️အောက်ကဇာတ်ကားအတွက် ပို့မည့် v1.0 Channel ရွေးချယ်ဖို့ လိုအပ်နေပါတယ်⚠️\n" + script_url)
        if len(chck_rtd) != 0:
            if ("Not Rated" not in chck_rtd) or ("R" == chck_rtd):
                Trnl.sh2.update('J2', channels.rt_chnl[0])
                Trnl.sh2.update('I2', channels.rt_chnl[1])
        if len(ctry) != 0:
            if "India" in ctry:
                Trnl.sh2.update('J2', channels.bt_chnl[0])
                Trnl.sh2.update('I2', channels.bt_chnl[1])
        if 'Country' in omdb_req:
            if len(omdb_req['Country']) != 0:
                if "India" in omdb_req['Country']:
                    Trnl.sh2.update('J2', channels.bt_chnl[0])
                    Trnl.sh2.update('I2', channels.bt_chnl[1])
        if len(mv_gnr) != 0:
            if "Animation" in mv_gnr:
                Trnl.sh2.update('J2', channels.ani_chnl[0])
                Trnl.sh2.update('I2', channels.ani_chnl[1])
        for all in soup.select('#single > div.content.right > div.sheader > div.poster > img'):
            vlink = all['src']
        phto_splt = vlink.split('/')
        vtext = ""
        try:
            bd_lks = []
            bd_soup = soup.select('#info > div.wp-content')
            for all in bd_soup:
                bd_lks.append(all.text)
            if len(bd_lks) != 0:
                vtext = "\n".join([str(txt) for txt in bd_lks])
        except:
            if 'tvshows' in script_url:
                start1 = 'Synopsis  '
                end1 = '   Original title'
            if 'tvshows' not in script_url:
                start1 = 'Synopsis  '
                end1 = '    Original title'
            vtext = (sscpt.split(start1))[1].split(end1)[0]
        if len(vtext) == 0:
            vtext = "⁉️"
        credit = 'Gold Channel Movies'
    if "channelmyanmar" in script_url:
        start3 = 'https://www.imdb.com/title/t'
        for all in soup.find_all('h1', {'itemprop': 'name'}):
            vcap = all.text
        year = ""
        try:
            year = re.findall(r'(\d+)', vcap)[len(re.findall(r'(\d+)', vcap)) - 1]
        except:
            for all in soup.select('#uwee > div.data > p.meta > span:nth-child(1) > a'):
                year=all.text
        try:
            title = vcap.replace('(' + year + ')', '').strip()
        except:
            title = vcap
        rmv = ['(21+)', '{21+}', '[21+]', '(18+)', '{18+}', '[18+]']
        for r in rmv:
            if r in title:
                title = title.replace(r, '').strip()
        omdb_url = 'https://www.omdbapi.com/?t=' + urllib.parse.quote_plus(title) + '&y=' + year + '&apikey=39ecaf7'
        omdb_req = json.loads(requests.get(omdb_url).content.decode('utf8'))
        if 'close' in Trnl.sh2.acell('N7').value:
            imdb_id = ''
            imdb_lst = []
            for s in soup.find_all('a', href=True):
                imdb_lst.append(s['href'])
            for i in imdb_lst:
                if "https://www.imdb.com/title/" in i:
                    imdb_id = i.split('/')[-2]
        #if ('Error' not in omdb_req) and ('imdbID' in omdb_req) and (str(omdb_req['imdbID']) != 'N/A') and (imdb_id == ''):
            #imdb_id = omdb_req['imdbID']
            if imdb_id == '':
                imdb_wrn = "⚠️အောက်ပါဇာတ်လမ်းအတွက် IMDB ID လိုအပ်နေပါတယ်⚠️👇\n" + script_url
                Trnl.sh2.update('L3', imdb_wrn)
                imdb_id = google('{} {} imdb'.format(title,year))[0]
        if 'open' in Trnl.sh2.acell('N7').value:
            imdb_id = Trnl.sh2.acell('M7').value
        logger.info(imdb_id)
        imdb_url = 'https://www.imdb.com/title/' + imdb_id
        imdb_id = Trnl.sh2.update('M7',imdb_id)
        if 'Error' in omdb_req:
            omdb_url = 'https://www.omdbapi.com/?i=' + str(imdb_id) + '&apikey=39ecaf7'
            omdb_req = json.loads(requests.get(omdb_url).content.decode('utf8'))
        if 'Movie' in Trnl.sh2.acell('P3').value:
            results = search.movies({"query": title, "year": year})
            gnr = []
            for g in soup.select('p.meta > i'):
                gnr.append(g.text.replace('\xa0', ' '))
            if len(gnr) != 0:
                mv_gnr = gnr[0]
            if "Uncategorized" in mv_gnr:
                try:
                    mv_gnr = omdb_req['Genre']
                except:
                    mv_gnr = ""
                if (mv_gnr == "") or (mv_gnr == 'N/A'):
                    try:
                        genres = genre.movie_list()
                        gnr_lst = []
                        for result in results:
                            for g in genres:
                                if g.id in result.genre_ids:
                                    gnr_lst.append(g.name)
                        mv_gnr = ", ".join(g for g in gnr_lst)
                    except:
                        mv_gnr = '⁉️️'
            if "Adult" in mv_gnr:
                Trnl.sh2.update('J2', channels.rt_chnl[0])
                Trnl.sh2.update('I2', channels.rt_chnl[1])
            elif "Animation" in mv_gnr:
                Trnl.sh2.update('J2', channels.ani_chnl[0])
                Trnl.sh2.update('I2', channels.ani_chnl[1])
            elif "Bollywood" in mv_gnr:
                Trnl.sh2.update('J2', channels.bt_chnl[0])
                Trnl.sh2.update('I2', channels.bt_chnl[1])
            else:
                Trnl.sh2.update('J2', channels.gn_chnl[0])
                Trnl.sh2.update('I2', channels.gn_chnl[1])
                Trnl.sh2.update('H3',"⚠️အောက်ကဇာတ်ကားကို v1 ဇာတ်လမ်းစုံ ကို ပို့ပါမယ်⚠️\n" + script_url)
        if 'Series' in Trnl.sh2.acell('P3').value:
            genres = genre.tv_list()
            try:
                mv_gnr = omdb_req['Genre']
            except:
                mv_gnr = ""
            if (mv_gnr == "") or ('N/A' == mv_gnr):
                try:
                    results = search.tv_shows({"query": title, "year": year})
                    gnr_lst = []
                    for result in results:
                        for g in genres:
                            if g.id in result.genre_ids:
                                gnr_lst.append(g.name)
                    if len(gnr_lst) > 5:
                        mv_gnr = '⁉️️'
                    if len(gnr_lst) < 5:
                        mv_gnr = ", ".join(g for g in gnr_lst)
                except:
                    mv_gnr = '⁉️️'
        try:
            if "India" in omdb_req['Country']:
                Trnl.sh2.update('J2', channels.bt_chnl[0])
                Trnl.sh2.update('I2', channels.bt_chnl[1])
        except:
            pass
        try:
            rntm = omdb_req['Runtime'].split(' ', 2)[0]
            rntm = "{} နာရီ : {} မိနစ်".format(*divmod(int(rntm), 60))
        except:
            rntm = ""
        if rntm == "":
            try:
                for r in soup.select('#uwee > div.data > p.meta > span > i'):
                    rntm = r.text
            except:
                rntm = ""
        if rntm == "":
            rntm = '⁉️️'
        all_lks = []
        for all in soup.select('div > img'):
            all_lks.append(all['src'])
        ctry_lst = Translation.ctry_lst
        ctry = ''
        try:
            ctry = omdb_req['Country']
        except:
            xpth_ctry = tree.xpath('//*[@id="uwee"]/div[2]/p[4]/text()')
            mv_ctry = []
            if len(xpth_ctry) != 0:
                for x in xpth_ctry:
                    for y in ctry_lst:
                        if y in x:
                            mv_ctry.append(y)
            ctry = ", ".join(c for c in mv_ctry)
        if ctry == '':
            ctry = '⁉️'
        if "India" in ctry:
            Trnl.sh2.update('J2', channels.bt_chnl[0])
            Trnl.sh2.update('I2', channels.bt_chnl[1])
        bd_lks = []
        bd_soup = soup.select('#cap1 > p')
        for all in bd_soup:
            bd_lks.append(all.text)
        if len(bd_lks) != 0:
            vtext = "\n".join([str(txt) for txt in bd_lks])
        else:
            if 'tvshows' in script_url:
                start1 = 'Synopsis of '
                end1 = 'Translat'
            if 'tvshows' not in script_url:
                start1 = 'Complete cast'
                end1 = 'Download Nulled Scripts and Plugins'
            vtext = (sscpt.split(start1))[1].split(end1)[0]
            del_vtext = 'Your browser does not support the video tag.  '
            if del_vtext in vtext:
                vtext = vtext.replace(del_vtext, '')
        vcap = vcap
        vlink = all_lks[0]
        phto_splt = vlink.split('/')
        credit = 'Channel Myanmar'
    if "burmesesubtitles" in script_url:
        if 'tmdb' in vlink:
            phto_cd = phto_splt[-1]
            phto_url = 'https://image.tmdb.org/t/p/original/' + phto_cd
        else:
            phto_url = ""
    if "channelmyanmar" in script_url:
        if 'tmdb' in vlink:
            phto_cd = phto_splt[-1]
            phto_url = 'https://image.tmdb.org/t/p/original/' + phto_cd
        else:
            phto_url = ""
    if "goldchannel" in script_url:
        try:
            phto_cd = phto_splt[-1].replace('-200x300', '')
            phto_url = 'https://image.tmdb.org/t/p/original/' + phto_cd
        except:
            phto_url = ""
    if phto_url == "":
        try:
            phto_url = omdb_req["Poster"].replace('_SX300', '_FMjpg_UX1000_')
        except:
            phto_url = ""
    if (phto_url == "") or ('N/A' in phto_url):
        try:
            for result in results:
                phto_url = 'https://image.tmdb.org/t/p/original' + result.poster_path
        except:
            phto_url = ""
    if (phto_url == "") or ('N/A' in phto_url):
        try:
            imdb_req = requests.get(imdb_url)
            imdb_req.encoding = imdb_req.apparent_encoding
            imdb_html = imdb_req.text
            imdb_soup = BeautifulSoup(imdb_html, 'html.parser')
            imdb_hrf = []
            for all in imdb_soup.find_all('a', href=True):
                imdb_hrf.append(all['href'])
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
        except:
            phto_url = vlink
    if 'close' in Trnl.sh2.acell('C3').value:
        try:
            omdb_url = 'https://www.omdbapi.com/?i=' + str(imdb_id) + '&apikey=39ecaf7'
            omdb_req = json.loads(requests.get(omdb_url).content.decode('utf8'))
            phto_url = omdb_req["Poster"].replace('_SX300', '_FMjpg_UX1000_')
        except:
            pass
    if 'open' in Trnl.sh2.acell('C3').value:
        phto_url = Trnl.sh2.acell('C4').value
    fdmn_frame(phto_url)
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
        imdb = '⁉️️'
    vd_qlt = Trnl.sh2.acell('H2').value
    typ = Trnl.sh2.acell('P3').value
    Trnl.sh2.update('M4', rntm)
    Trnl.sh2.update('M3', mv_gnr)
    Trnl.sh2.update('M5', year)
    Trnl.sh2.update('M6', ctry)
    Trnl.sh2.update('M8', imdb)
    Trnl.sh2.update('C2', phto_url)
    Trnl.sh2.update('D2', vcap)
    if '⁉️' in [mv_gnr,year,ctry]:
        imdb_info(imdb_id)
    try:
        Trnl.sh2.update('D4',title)
        Trnl.sh2.update('D5',year)
    except:
        pass
    Trnl.sh2.update('F2', credit)
    vtext = vtext.strip()
    Trnl.sh2.update('O2', vtext)
    vcap_hsh = ''.join(e for e in vcap if e.isalnum())
    Trnl.sh2.update('E2', vcap_hsh)
