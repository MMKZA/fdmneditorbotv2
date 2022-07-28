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
        vlink = (wscpt.split(start2))[1].split(end2)[0] + '.jpg'
        phto_splt = vlink.split('/')
        Trnl.sh2.update('H3', "⚠️အောက်ကဇာတ်ကားအတွက် ပို့မည့် v2.0 Channel ရွေးချယ်ဖို့ လိုအပ်နေပါတယ်⚠️\n" + script_url)
    elif "channelmyanmar" in script_url:
        all_lks = []
        for all in soup.select('div > img'):
            all_lks.append(all['src'])
        gnr = []
        for g in soup.select('p.meta > i'):
            gnr.append(g.text.replace('\xa0', ''))
        if len(gnr) != 0:
            mv_gnr = gnr[0] + " | "
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
                Trnl.sh2.update('H3', "⚠️အောက်ကဇာတ်ကားအတွက် ပို့မည့် v1.0 Channel ရွေးချယ်ဖို့ လိုအပ်နေပါတယ်⚠️\n" + script_url)
        else:
            mv_gnr = ""
        Trnl.sh2.update('M3', mv_gnr)
        ctry_lst = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola',
                    'Anguilla',
                    'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria',
                    'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize',
                    'Benin',
                    'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba',
                    'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory',
                    'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada',
                    'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China',
                    'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo',
                    'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia',
                    'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica',
                    'Dominican Republic',
                    'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia',
                    'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana',
                    'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana',
                    'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey',
                    'Guinea',
                    'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands',
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
                    'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands',
                    'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island',
                    'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau',
                    'Palestinian Territory, Occupied',
                    'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal',
                    'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy',
                    'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia',
                    'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines',
                    'Samoa',
                    'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles',
                    'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands',
                    'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka',
                    'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland',
                    'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of',
                    'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey',
                    'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
                    'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan',
                    'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British',
                    'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
        ctry = []
        for c in soup.select('p', {'class': 'icon-network'}):
            ctry.append(c.text)
        if len(ctry) != 0:
            for x in ctry:
                for y in ctry_lst:
                    if y in x:
                        mv_ctry = y
                        if "India" in mv_ctry:
                            Trnl.sh2.update('J2', '-1001718578294')
                            Trnl.sh2.update('I2', 'https://t.me/c/1718578294/')
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
            start2 = 'image" src="'
            end2 = '.jpg'
            vtext = (sscpt.split(start1))[1].split(end1)[0]
            del_vtext = 'Your browser does not support the video tag.  '
            if del_vtext in vtext:
                vtext = vtext.replace(del_vtext, '')
        vcap = sscpt.split('\n', 1)[0]
        vlink = all_lks[0]
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
        vd_qlt = Trnl.sh2.acell('H2').value
        Trnl.sh2.update('A2', vcap + " | " + mv_gnr + vd_qlt + "\n\nဇာတ်ညွှန်း 📜\n\n" + vtext)
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
        if "goldchannel" in script_url:
            credit = 'Gold Channel Movies'
        elif "channelmyanmar" in script_url:
            credit = 'Channel Myanmar'
        Trnl.sh2.update('F2', credit)
        msg_whl = phto_url + "\n\n" + vcap + " | " + mv_gnr + "\n\nဇာတ်ညွှန်း 📜\n\n" + vtext
        msg_trm = msg_whl[0:4095]
        Trnl.sh2.update('O2', msg_trm)
