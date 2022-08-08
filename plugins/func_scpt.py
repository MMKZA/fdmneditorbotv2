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
    # override encoding by real educated guess as provided by chardet
    req.encoding = req.apparent_encoding
    # access the data
    html_text = req.text
    soup = BeautifulSoup(html_text, 'html.parser')
    wscpt = soup.prettify()
    sscpt = soup.get_text()
    tmdb = TMDb()
    tmdb.api_key = "53b9eff4684ba49f0f2225d888fd4202"
    search = Search()
    genre = Genre()
    if "burmalinkchannel" in script_url:
        jsn1 = json.loads(html_text)
        html = json2html.convert(json=jsn1)
        soup = BeautifulSoup(html, 'html.parser')
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
            rntm = "{} hr: {} min".format(*divmod(int(rntm), 60))
        except:
            rntm = ""
        if rntm == "":
            try:
                rntm = omdb_req['Runtime'].split(' ', 2)[0]
                rntm = "{} hr:{} min".format(*divmod(int(rntm), 60))
            except:
                rntm = '⁉'
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
                mv_gnr = "⁉"
        # GENRE_RELATED
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
            Trnl.sh2.update('H3', "⚠️အောက်ကဇာတ်ကားကို v1 ဇာတ်လမ်းစုံ ကို ပို့ပါမယ်⚠️\n" + script_url)
        # COUNTRY
        ctry = soup.find("th", text="reCountry").find_next_sibling("td").text
        # COUNTRY_RELATED
        if len(ctry) != 0:
            if ("India" in ctry) or ("india" in ctry):
                Trnl.sh2.update('J2', '-1001718578294')
                Trnl.sh2.update('I2', 'https://t.me/c/1718578294/')
        if 'Country' in omdb_req:
            if len(omdb_req['Country']) != 0:
                if "India" in omdb_req['Country']:
                    Trnl.sh2.update('J2', '-1001718578294')
                    Trnl.sh2.update('I2', 'https://t.me/c/1718578294/')
        # POSTER
        try:
            phto_url = omdb_req["Poster"].replace('_SX300', '')
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
        for all in soup.select('#single > div.content.right > div.sheader > div.data > h1'):
            vcap = all.text
        for all in soup.select('#single > div.content.right > div.sheader > div.data > div.extra > span.date'):
            rls_date = datetime.datetime.strptime(all.text, "%b. %d, %Y")
            year = rls_date.year
        omdb_url = 'https://www.omdbapi.com/?t=' + urllib.parse.quote_plus(vcap) + '&y=' + str(year) + '&apikey=39ecaf7'
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
                mv_gnr = "⁉️"
        try:
            if 'tvshows' in script_url:
                for all in soup.select('#info > div:nth-child(9) > span'):
                    rntm = all.text.split(' ', 2)[0]
                    rntm = "{} hr:{} min".format(*divmod(int(rntm), 60))
            if 'movies' in script_url:
                for all in soup.select(
                        '#single > div.content.right > div.sheader > div.data > div.extra > span.runtime'):
                    rntm = all.text.split(' ', 2)[0]
                    rntm = "{} hr:{} min".format(*divmod(int(rntm), 60))
        except:
            rntm = ""
        if rntm == "":
            try:
                rntm = omdb_req['Runtime'].split(' ', 2)[0]
                rntm = "{} hr:{} min".format(*divmod(int(rntm), 60))
            except:
                rntm = ""
        if rntm == "":
            rntm = '⁉️'
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
        Trnl.sh2.update('J2', '-1001785695486')
        Trnl.sh2.update('I2', 'https://t.me/c/1785695486/')
        Trnl.sh2.update('H3', "⚠️အောက်ကဇာတ်ကားအတွက် ပို့မည့် v1.0 Channel ရွေးချယ်ဖို့ လိုအပ်နေပါတယ်⚠️\n" + script_url)
        if len(chck_rtd) != 0:
            if ("Not Rated" not in chck_rtd) or ("R" == chck_rtd):
                Trnl.sh2.update('J2', '-1001750623132')
                Trnl.sh2.update('I2', 'https://t.me/c/1750623132/')
        if len(ctry) != 0:
            if "India" in ctry:
                Trnl.sh2.update('J2', '-1001718578294')
                Trnl.sh2.update('I2', 'https://t.me/c/1718578294/')
        if 'Country' in omdb_req:
            if len(omdb_req['Country']) != 0:
                if "India" in omdb_req['Country']:
                    Trnl.sh2.update('J2', '-1001718578294')
                    Trnl.sh2.update('I2', 'https://t.me/c/1718578294/')
        if len(mv_gnr) != 0:
            if "Animation" in mv_gnr:
                Trnl.sh2.update('J2', '-1001389311243')
                Trnl.sh2.update('I2', 'https://t.me/c/1389311243/')
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
            vtext = "⁉"
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
        if 'Movie' in Trnl.sh2.acell('P3').value:
            results = search.movies({"query": title, "year": year})
            gnr = []
            for g in soup.select('p.meta > i'):
                gnr.append(g.text.replace('\xa0', ''))
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
            imdb_hrf = []
            for h in soup.find_all('a',href=True):
                imdb_hrf.append(h['href'])
            for h in imdb_hrf:
                if "https://www.imdb.com/title/t" in h:
                    imdb_url = h
                    imdb_id = imdb_url.split('/', 5)[4]
        except:
            imdb_id = omdb_req['imdbID']
            if (len(imdb_id) != 0) and ('NA' not in imdb_id):
                imdb_url = 'https://www.imdb.com/title/' + imdb_id
        try:
            omdb_req = omdb_req
        except:
            hrf_lks = []
            for all in soup.find_all('a', href=True):
                hrf_lks.append(all['href'])
            for h in hrf_lks:
                omdb_url = 'https://www.omdbapi.com/?i=' + imdb_id + '&apikey=39ecaf7'
                omdb_req = json.loads(requests.get(omdb_url).content.decode('utf8'))
        try:
            if "India" in omdb_req['Country']:
                Trnl.sh2.update('J2', '-1001718578294')
                Trnl.sh2.update('I2', 'https://t.me/c/1718578294/')
        except:
            pass
        try:
            rntm = omdb_req['Runtime'].split(' ', 2)[0]
            rntm = "{} hr:{} min".format(*divmod(int(rntm), 60))
        except:
            rntm = ""
        if rntm == "":
            try:
                for r in soup.select('#uwee > div.data > p.meta > span > i'):
                    rntm = r.text
            except:
                rntm = ""
        if rntm == "":
            rntm = '⁉️'
        all_lks = []
        for all in soup.select('div > img'):
            all_lks.append(all['src'])
        ctry_lst = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola',
                    'Anguilla',
                    'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria',
                    'Azerbaijan',
                    'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda',
                    'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba',
                    'Bosnia and Herzegovina',
                    'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam',
                    'Bulgaria',
                    'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands',
                    'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands',
                    'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands',
                    'Costa Rica',
                    "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti',
                    'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea',
                    'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France',
                    'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia',
                    'Germany',
                    'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala',
                    'Guernsey',
                    'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands',
                    'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India',
                    'Indonesia',
                    'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica',
                    'Japan',
                    'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of",
                    'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia',
                    'Lebanon',
                    'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao',
                    'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta',
                    'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
                    'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro',
                    'Montserrat',
                    'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia',
                    'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island',
                    'Northern Mariana Islands',
                    'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama',
                    'Papua New Guinea',
                    'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar',
                    'Réunion',
                    'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy',
                    'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia',
                    'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines',
                    'Samoa',
                    'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles',
                    'Sierra Leone',
                    'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia',
                    'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan',
                    'Suriname',
                    'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland',
                    'Syrian Arab Republic',
                    'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand',
                    'Timor-Leste',
                    'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
                    'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
                    'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu',
                    'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.',
                    'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
        ctry_all = []
        for c in soup.select('p', {'class': 'icon-network'}):
            ctry_all.append(c.text)
        if len(ctry_all) != 0:
            for x in ctry_all:
                for y in ctry_lst:
                    if y in x:
                        mv_ctry = y
                        if "India" in mv_ctry:
                            Trnl.sh2.update('J2', '-1001718578294')
                            Trnl.sh2.update('I2', 'https://t.me/c/1718578294/')
        try:
            if 'Country' in omdb_req:
                ctry = omdb_req['Country']
        except:
            ctry = '⁉'
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
            phto_url = omdb_req["Poster"].replace('_SX300', '')
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
    vd_qlt = Trnl.sh2.acell('H2').value
    typ = Trnl.sh2.acell('P3').value
    Trnl.sh2.update('M4', rntm)
    Trnl.sh2.update('M3', mv_gnr)
    Trnl.sh2.update('M5', year)
    Trnl.sh2.update('M6', ctry)
    Trnl.sh2.update('A2', vcap + "\n\n🎬 " + mv_gnr + "\n🗓️ " + str(year) + " 🎞️ " + typ + " 📺 " + vd_qlt + "\n⏰ " + rntm + "\n🌎 " + ctry + "\n\nဇာတ်ညွှန်း 📜\n\n" + vtext.strip())
    Trnl.sh2.update('C2', phto_url)
    Trnl.sh2.update('D2', vcap)
    vcap_hsh = ''.join(e for e in vcap if e.isalnum())
    if 'ChannelMyanmar' in vcap_hsh:
        vcap_hsh = vcap_hsh.replace('ChannelMyanmar', '')
    elif 'GoldChannelMovies' in vcap_hsh:
        vcap_hsh = vcap_hsh.replace('GoldChannelMovies', '')
    else:
        vcap_hsh = vcap_hsh
    Trnl.sh2.update('E2', vcap_hsh)
    Trnl.sh2.update('F2', credit)
    vcap = '<b>' + vcap + '</b>'
    msg_whl = phto_url + "\n\n" + vcap + "\n\n🎬 " + mv_gnr + "\n🗓️ " + str(year) + " 🎞️ " + typ + " 📺 " + vd_qlt + "\n⏰ " + rntm + "\n🌎 " + ctry + "\n\nဇာတ်ညွှန်း 📜\n\n" + vtext.strip()
    msg_trm = msg_whl[0:4095]
    Trnl.sh2.update('O2', msg_trm)
