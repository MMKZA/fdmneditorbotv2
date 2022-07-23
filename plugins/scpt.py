import logging
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

import requests
from bs4 import BeautifulSoup
from translation import Translation
import pyrogram
from pyrogram.types.bots_and_keyboards import InlineKeyboardButton, InlineKeyboardMarkup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

logging.getLogger("pyrogram").setLevel(logging.WARNING)
from trnl import Trnl
@pyrogram.Client.on_message(pyrogram.filters.command(["scpt"]))
async def script_call_back(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        script_url = Trnl.sh1.acell('M3').value
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
        Trnl.sh1.update('A2', vcap + "\n\nဇာတ်ညွှန်း 📜\n\n" + vtext)
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
        scpt_msg = await bot.send_message(
            chat_id="@fdmnscripts",
            text=msg_trm,
        )
        scpt_id = scpt_msg.message_id
        vtext_lk = "https://t.me/fdmnscripts/" + str(scpt_id)
        vtext_hplk = '<a href="' + vtext_lk + '">👉 ဇာတ်ညွှန်းဖတ်ရန် နှိပ်ပါ 📜</a>'
        chnl_lk = str(Trnl.sh1.acell('I3').value)
        vd_lk = chnl_lk + str(Trnl.sh1.acell('H3').value)
        vd_hplk = '<a href="' + vd_lk + '">👉 ဇာတ်လမ်းကြည့်ရန် နှိပ်ပါ 🍿</a>'
        invt_lst = [
            "https://t.me/+RqwAss5VI6M0N2Rl",
            "https://t.me/+Hlpn-6_fi8c1OWI1",
            "https://t.me/+fYTgNiUsRaJlY2Y1",
            "https://t.me/+rg5dEnd2JgFiMTll"
        ]
        id_lst = [
            "-1001785695486",
            "-1001718578294",
            "-1001389311243",
            "-1001750623132"
        ]
        if Trnl.sh1.acell('J2').value == id_lst[0]:
          invt_lk = invt_lst[0]
        if Trnl.sh1.acell('J2').value == id_lst[1]:
          invt_lk = invt_lst[1]
        if Trnl.sh1.acell('J2').value == id_lst[2]:
          invt_lk = invt_lst[2]
        if Trnl.sh1.acell('J2').value == id_lst[3]:
          invt_lk = invt_lst[3]
        chnl_hplk = '<a href="' + invt_lk + '">👉 Channel Join ရန်နှိပ်ပါ 🔗</a>'
        mchnl_msg = await bot.send_photo(
            "@fdmnchannel",
            phto_url,
            "🎞️\n" + vcap + "\n\n" + chnl_hplk + "\n\n" + vtext_hplk + "\n\n" + vd_hplk + "\n\n" + Translation.CHNL_JOIN,
            'html'
        )
        Trnl.sh1.update('G2', mchnl_msg.message_id)
        await bot.send_message(
            chat_id=update.chat.id,
            text="Post တင်လိုက်သော ဇာတ်လမ်း 👇\n" + script_url
        )
