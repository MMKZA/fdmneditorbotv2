import os
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
    
from translation import Translation
import pyrogram
from trnl import Trnl
import asyncio
from plugins.ytsn_dllk import ytsn_dllk
from plugins.gdrvclean import gdrvclean
from plugins.transloader import transloader
from plugins.gdrvclean import gdrvclean
from plugins.gdrvclean import poster_gdrvclean
from plugins.func_scpt import func_scpt
from plugins.series import series
from plugins.echo_auto import echo_auto
import requests, zipfile, io
import subprocess
import json

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
@pyrogram.Client.on_message(pyrogram.filters.command(["trsl"]))
def trsl_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        if '|' in update.reply_to_message.text:
            lk = update.reply_to_message.text.split("|")[0].strip()
        else:
            lk = update.reply_to_message.text
        if "yoteshinportal.cc" in lk:
            gdrv_retrn = ytsn_dllk(lk)
            if "error" in gdrv_retrn:
                gdrvclean(gdrv_retrn)
                gdrv_lk = ytsn_dllk(lk)
            else:
                gdrv_lk = gdrv_retrn
        elif "mega.nz" in lk:
            gdrv_lk = lk
        elif "https://drive.google.com/" in lk:
            gdrv_lk = lk
        elif "burmesesubtitles.com" in lk:
            gdrv_lk = lk
        base = Trnl.sh2.acell('K2').value
        final_link = transloader(base, gdrv_lk)
        Trnl.sh2.update('L2', final_link)
        arc_kw = ['.zip','.rar','.7z']
        vd_kw = ['.mp4','.mkv','.mov','.m4v']
        fl_ext = os.path.splitext(final_link)[1]
        if fl_ext in arc_kw:
            text = "Archive ဖိုင်အမျိုးအစားဖြစ်ပါတယ်၊ 🗃️SFile ကိုရွေးချယ်ပါ 👇\n"
            bot.send_message(
                chat_id=update.chat.id,
                text=text + final_link
            )
            asyncio.run(echo_auto(bot,update,final_link))
        elif fl_ext in vd_kw:
            text = "Video ဖိုင်အမျိုးအစားဖြစ်ပါတယ်၊ 📺SVideo ကိုရွေးချယ်ပါ 👇\n"
            bot.send_message(
                chat_id=update.chat.id,
                text=text + final_link
            )
            asyncio.run(echo_auto(bot,update,final_link))
        else:
            text = "Link အမှားအယွင်းရှိနိုင်ပါတယ်၊ သေချာစစ်ကြည့်ပါ ⚠️\n"
            bot.send_message(
                chat_id=update.chat.id,
                text=text + final_link
            )
        
@pyrogram.Client.on_message(pyrogram.filters.command(["gtsh"]))
def gtsh_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        lk = update.reply_to_message.text
        Trnl.sh2.update('L2', lk)
 
@pyrogram.Client.on_message(pyrogram.filters.command(["srs"]))
def srs_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        web_url = update.reply_to_message.text
        
        source_kw_lst = ['https://channelmyanmar.org/','https://goldchannel.net/']
        act_source_kw = ''
        for source_kw in source_kw_lst:
            if source_kw in web_url:
                act_source_kw = source_kw
                
        if act_source_kw in web_url:
            Trnl.sh2.update('M2', web_url)
            Trnl.sh2.update('P3', "Series")
            if "goldchannel" in act_source_kw:
                func_scpt(web_url)
                if web_url in Trnl.sh2.acell('L3').value:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=Trnl.sh2.acell('L3').value
                    )
                epsd_lst = series(web_url)
                translator = Translator()
                en_cap = Trnl.sh2.acell('D2').value
                mm_cap = translator.translate(en_cap,'my','en').text
                bot.send_message(
                    chat_id=update.chat.id,
                    text=en_cap
                )
                bot.send_message(
                    chat_id=update.chat.id,
                    text=mm_cap
                )
                bot.send_message(
                    chat_id=update.chat.id,
                    text="Episodes အားလုံး 👇"
                )
                for epsd in epsd_lst:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=epsd,
                        disable_web_page_preview=True
                    )
            if "channelmyanmar" in act_source_kw:
                func_scpt(web_url)
                if web_url in Trnl.sh2.acell('L3').value:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=Trnl.sh2.acell('L3').value
                    )
                if web_url in Trnl.sh2.acell('H3').value:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=Trnl.sh2.acell('H3').value
                    )
                epsd_lst = series(web_url)
                translator = Translator()
                en_cap = Trnl.sh2.acell('D2').value
                mm_cap = translator.translate(en_cap,'my','en').text
                bot.send_message(
                    chat_id=update.chat.id,
                    text=en_cap
                )
                bot.send_message(
                    chat_id=update.chat.id,
                    text=mm_cap
                )
                if len(epsd_msg) == 3:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="Yoteshin Episodes အားလုံး 👇"
                    )
                    for epsd in epsd_lst[0]:
                        bot.send_message(
                            chat_id=update.chat.id,
                            text=epsd,
                            disable_web_page_preview=True
                        )
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="Mega Episodes အားလုံး 👇"
                    )
                    for epsd in epsd_lst[1]:
                        bot.send_message(
                            chat_id=update.chat.id,
                            text=epsd,
                            disable_web_page_preview=True
                        )
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="နောက်ဆုံးတင်ထားသော Episodes များ 👇"
                    )
                    for epsd in epsd_lst[2]:
                        bot.send_message(
                            chat_id=update.chat.id,
                            text=epsd,
                            disable_web_page_preview=True
                        )
                if len(epsd_msg) == 2:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="Yoteshin Episodes အားလုံး 👇"
                    )
                    for epsd in epsd_lst[0]:
                        bot.send_message(
                            chat_id=update.chat.id,
                            text=epsd,
                            disable_web_page_preview=True
                        )
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="နောက်ဆုံးတင်ထားသော Episodes များ 👇"
                    )
                    for epsd in epsd_lst[2]:
                        bot.send_message(
                            chat_id=update.chat.id,
                            text=epsd,
                            disable_web_page_preview=True
                        )
@pyrogram.Client.on_message(pyrogram.filters.command(["ytdlp"]))
def ytdlpdl_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        zip_file_url = 'https://github.com/yt-dlp/yt-dlp/archive/refs/heads/master.zip'
        r = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        dl_dir = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/ytdlp"
        z.extractall(dl_dir)
        cd_dir  = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/ytdlp/yt-dlp-master/"
        with cd(cd_dir):
             process = subprocess.run(['python', 'setup.py', 'install'],shell=False)
        bot.send_message(
            chat_id=update.chat.id,
            text="လုပ်ဆောင်ချက်အောင်မြင်ပါတယ်"
        )

@pyrogram.Client.on_message(pyrogram.filters.command(["ffmpeg"]))
def ffmpegdl_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        zip_file_url = 'https://github.com/kkroening/ffmpeg-python/archive/refs/heads/master.zip'
        r = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        dl_dir = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/ffmpeg"
        z.extractall(dl_dir)
        cd_dir  = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/ffmpeg/ffmpeg-python-master/"
        with cd(cd_dir):
             process = subprocess.run(['python', 'setup.py', 'install'],shell=False)
        bot.send_message(
            chat_id=update.chat.id,
            text="လုပ်ဆောင်ချက်အောင်မြင်ပါတယ်"
        )

@pyrogram.Client.on_message(pyrogram.filters.command(["jsdl"]))
def jsdl_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        zip_file_url = Trnl.sh2.acell('U2').value
        r = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        dl_dir = Config.DOWNLOAD_LOCATION + "/myjsons"
        z.extractall(dl_dir)
        bot.send_message(
            chat_id=update.chat.id,
            text="လုပ်ဆောင်ချက်အောင်မြင်ပါတယ်"
        )

@pyrogram.Client.on_message(pyrogram.filters.command(["cl"]))
def clean(bot, update):
    status = "error"
    gdrvclean(status)
    bot.delete_messages(
        chat_id=update.chat.id,
        message_ids=update.message_id
    )
    
@pyrogram.Client.on_message(pyrogram.filters.command(["pstcl"]))
def poster_clean(bot, update):
    poster_gdrvclean()
    bot.delete_messages(
        chat_id=update.chat.id,
        message_ids=update.message_id
    )
@pyrogram.Client.on_message(pyrogram.filters.command(["openauto"]))
def openauto_vlink(bot, update):
    Trnl.sh2.update('C3','open')
    imdb_id = Trnl.sh2.acell('M7').value
    imdb_url = 'https://www.imdb.com/title/' + imdb_id
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
    Trnl.sh2.update('C4',phto_url)
    web_url = Trnl.sh2.acell('M2').value
    func_scpt(web_url)
    bot.send_message(
        chat_id=update.chat.id,
        text="လုပ်ဆောင်ချက်အောင်မြင်ပါတယ်"
    )
@pyrogram.Client.on_message(pyrogram.filters.command(["open"]))
def open_vlink(bot, update):
    Trnl.sh2.update('C3','open')
    phto_url = update.reply_to_message.text
    Trnl.sh2.update('C4',phto_url)
    web_url = Trnl.sh2.acell('M2').value
    func_scpt(web_url)
    bot.send_message(
        chat_id=update.chat.id,
        text="လုပ်ဆောင်ချက်အောင်မြင်ပါတယ်"
    )
