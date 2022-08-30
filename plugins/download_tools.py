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
from plugins.func_scpt import func_scpt
from plugins.series import series
from plugins.echo_auto import echo_auto
import requests, zipfile, io
import subprocess
import os

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
        base = Trnl.sh4.acell('K2').value
        final_link = transloader(base, gdrv_lk)
        Trnl.sh4.update('L2', final_link)
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
        Trnl.sh4.update('L2', lk)
 
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
            Trnl.sh4.update('M2', web_url)
            Trnl.sh4.update('P3', "Series")
            if "goldchannel" in act_source_kw:
                func_scpt(web_url)
                if web_url in Trnl.sh4.acell('L3').value:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=Trnl.sh4.acell('L3').value
                    )
                epsd_lst = series(web_url)
                translator = Translator()
                en_cap = Trnl.sh4.acell('D2').value
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
                if web_url in Trnl.sh4.acell('L3').value:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=Trnl.sh4.acell('L3').value
                    )
                if web_url in Trnl.sh4.acell('H3').value:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=Trnl.sh4.acell('H3').value
                    )
                epsd_lst = series(web_url)
                translator = Translator()
                en_cap = Trnl.sh4.acell('D2').value
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
@pyrogram.Client.on_message(pyrogram.filters.command(["ytdlpdl"]))
def ytdlpdl_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        zip_file_url = 'https://github.com/yt-dlp/yt-dlp/archive/refs/heads/master.zip'
        r = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        dl_dir = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/ytdlp"
        z.extractall(dl_dir)
        bot.send_message(
            chat_id=update.chat.id,
            text="လုပ်ဆောင်ချက်အောင်မြင်ပါတယ်"
        )
@pyrogram.Client.on_message(pyrogram.filters.command(["ytdlpstp"]))
def ytdlpstp_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        cd_dir  = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/ytdlp/yt-dlp-master/"
        with cd(cd_dir):
             process = subprocess.run(['python', 'setup.py', 'install'],shell=False)
        bot.send_message(
            chat_id=update.chat.id,
            text="လုပ်ဆောင်ချက်အောင်မြင်ပါတယ်"
        )
@pyrogram.Client.on_message(pyrogram.filters.command(["ffmpegdl"]))
def ytdlpdl_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        zip_file_url = 'https://github.com/kkroening/ffmpeg-python/archive/refs/heads/master.zip'
        r = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        dl_dir = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/ffmpeg"
        z.extractall(dl_dir)
        bot.send_message(
            chat_id=update.chat.id,
            text="လုပ်ဆောင်ချက်အောင်မြင်ပါတယ်"
@pyrogram.Client.on_message(pyrogram.filters.command(["ffmpegstp"]))
def ytdlpstp_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
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
        zip_file_url = update.reply_to_message.text
        r = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        dl_dir = Config.DOWNLOAD_LOCATION + "/myjsons"
        z.extractall(dl_dir)
        bot.send_message(
            chat_id=update.chat.id,
            text="လုပ်ဆောင်ချက်အောင်မြင်ပါတယ်"
        )
