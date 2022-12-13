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
from plugins.gdrvclean import gdrvclean, gdtotclean
from plugins.transloader import transloader
from plugins.gdrvclean import gdrvclean
from plugins.gdrvclean import poster_gdrvclean
from plugins.func_scpt import func_scpt
from plugins.series import series
from plugins.echo_auto import echo_auto
from plugins.echo_echo import echo_echo
from plugins.extract_list_upload import extract_list_upload
from plugins.methods import methods,plhh_method,transload_method,direct_method
from helper_funcs.fdmn_frame import fdmn_frame
from helper_funcs.imdb_search import google, channelmyanmar
import requests, zipfile, io
import subprocess
import json
from bs4 import BeautifulSoup
from googletrans import Translator
import re
from datetime import datetime, timedelta
from channels import channels

def convert(seconds):
    day = int(seconds // (24*3600))
    seconds %= 24 * 3600
    hour = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60 
    return "{:d} ရက် : {:d} နာရီ".format(day, hour)

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

@pyrogram.Client.on_message(pyrogram.filters.regex(pattern="\Aဖိုင်စာရင်း"))
def upload_from_dir(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        lst_txt = update.text
        lst = lst_txt.split('\n')
        lst.pop(0)
        ttl = len(lst)
        a = bot.send_message(
            chat_id=update.from_user.id,
            text='စုစုပေါင်းဖိုင် {} ခုကိုတင်ဖို့ ပြင်ဆင်နေပါတယ်...'.format(ttl),
            reply_to_message_id=update.message_id
        )
        for dir in lst:
            nth = lst.index(dir) + 1
            b = a.edit_text(text='စုစုပေါင်း {} ခုမှာ {} ခုမြောက်ကို တင်နေပါတယ်...'.format(ttl, nth))
            extract_list_upload(bot, update, dir)
        b.edit_text(text='စုစုပေါင်း {} ခုကို အောင်မြင်စွာတင်ပြီးပါပြီ...'.format(ttl))
@pyrogram.Client.on_message(pyrogram.filters.regex(pattern="\Aတင်မယ့်စာရင်း"))
def upload_by_list(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        lst_txt = update.text
        lst = lst_txt.split('\n')
        lst.pop(0)
        ttl = len(lst)
        a = bot.send_message(
            chat_id=update.from_user.id,
            text='စုစုပေါင်းဖိုင် {} ခုကိုတင်ဖို့ ပြင်ဆင်နေပါတယ်...'.format(ttl),
            reply_to_message_id=update.message_id
        )
        base = Trnl.sh2.acell('K2').value
        for lk in lst:
            if 'megaup.net' in lk and '?download_token=' in lk:
                nth = lst.index(lk) + 1
                b = a.edit_text(text='စုစုပေါင်း {} ခုမှာ {} ခုမြောက်ကို တင်နေပါတယ်...'.format(ttl, nth))
                fl_fll_nm = lk.split('/')[4].split('?download_token')[0]
                vd_kw = ['.mkv','.m4a','.mov','.avi']
                vd_ext = os.path.splitext(fl_fll_nm)[1]
                if vd_ext != '' and vd_ext in vd_kw:
                    fl_fll_nm = fl_fll_nm.replace(vd_ext,'.mp4')
                Trnl.sh2.update('D6',fl_fll_nm)
                final_link = transloader(base, lk)
                Trnl.sh2.update('L2', final_link)
                vd_fl_kw = ['.mp4','.mkv','.mov','.m4v','.avi']
                fl_ext = os.path.splitext(final_link)[1]
                if fl_ext in vd_fl_kw:
                    text = "Video ဖိုင်အမျိုးအစားဖြစ်ပါတယ်၊ 📺SVideo ကိုရွေးချယ်ပါ 👇\n"
                    mssg = bot.send_message(
                        chat_id=update.from_user.id,
                        text=text + final_link
                    )
                    echo_echo(bot,update,final_link,mssg,mssg.message_id)
                else:
                    text = "Link အမှားအယွင်းရှိနိုင်ပါတယ်၊ သေချာစစ်ကြည့်ပါ ⚠️\n"
                    bot.send_message(
                        chat_id=update.from_user.id,
                        text=text + final_link
                    )
                    echo_echo(bot,update,final_link,mssg,mssg.message_id)            
        b.edit_text(text='စုစုပေါင်း {} ခုကို အောင်မြင်စွာတင်ပြီးပါပြီ...'.format(ttl))
        
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
        else:
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
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )            
@pyrogram.Client.on_message(pyrogram.filters.command(["gtsh"]))
def gtsh_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        lk = update.reply_to_message.text
        Trnl.sh2.update('L2', lk)
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        ) 
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
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
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
    if update.from_user.id in Config.AUTH_USERS:
        status = "error"
        gdrvclean(status)
        gdtotclean(status)
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )    
@pyrogram.Client.on_message(pyrogram.filters.command(["pstcl"]))
def poster_clean(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        poster_gdrvclean()
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )

@pyrogram.Client.on_message(pyrogram.filters.command(["offimdbpy"]))
def open_imdbpy(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        Trnl.sh2.update('C3','open')
        web_url = Trnl.sh2.acell('M2').value
        #func_scpt(web_url)
        #Trnl.sh2.update('C3','close')
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )    
@pyrogram.Client.on_message(pyrogram.filters.command(["onimdbpy"]))
def close_imdbpy(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        Trnl.sh2.update('C3','close')
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )

@pyrogram.Client.on_message(pyrogram.filters.command(["deadimdbpy"]))
def open_imdb(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        Trnl.sh2.update('N7','open')
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )    
@pyrogram.Client.on_message(pyrogram.filters.command(["refreshimdb"]))
def close_imdb(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        Trnl.sh2.update('N7','close')
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
    
@pyrogram.Client.on_message(pyrogram.filters.command(["imdbgoogle"]))
def imdb_google(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        try:
            title = Trnl.sh2.acell('D4').value
            year = Trnl.sh2.acell('D5').value
        except:
            vcap = Trnl.sh2.acell('D2').value
            year = ''
            year = re.findall(r'(\d+)', vcap)[len(re.findall(r'(\d+)', vcap)) - 1]
            title = vcap.replace('(' + year + ')', '').strip()
        imdb_rtrn = google('{} {} imdb'.format(title,year))
        imdb_id = imdb_rtrn[0]
        imdb_lst = imdb_rtrn[1]
        imdb_url = 'https://www.imdb.com/title/' + imdb_id
        bot.send_message(
            chat_id=update.chat.id,
            text="Result အားလုံး 👇"
        )  
        for imdb in imdb_lst:
            bot.send_message(
                chat_id=update.chat.id,
                text=imdb
            )        
        bot.send_message(
            chat_id=update.chat.id,
            text="အဖြစ်နိုင်ဆုံး 👇"+imdb_url
        )
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
@pyrogram.Client.on_message(pyrogram.filters.command(["autoauto"]))
def auto_auto(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        Trnl.sh2.update('V2','auto')
        Trnl.sh2.update('W2','auto')
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
@pyrogram.Client.on_message(pyrogram.filters.command(["manualmanual"]))
def manual_manual(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        Trnl.sh2.update('V2','manual')
        Trnl.sh2.update('W2','manual')
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
@pyrogram.Client.on_message(pyrogram.filters.command(["autoplm"]))
def auto_plm(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        Trnl.sh2.update('W2','auto')
        Trnl.sh2.update('W3','method=PLM')
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
@pyrogram.Client.on_message(pyrogram.filters.command(["autotm"]))
def auto_tm(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        Trnl.sh2.update('W2','auto')
        Trnl.sh2.update('W3','method=TM')
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
@pyrogram.Client.on_message(pyrogram.filters.command(["autodm"]))
def auto_dm(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        Trnl.sh2.update('W2','auto')
        Trnl.sh2.update('W3','method=DM')
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )    
@pyrogram.Client.on_message(pyrogram.filters.command(["upld"]))
def upld_tool(bot, update):
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
        else:
            gdrv_lk = lk
        gdrv_id = gdrv_lk.split('/')[5]
        #logger.info(gdrv_id)
        Trnl.sh2.update('L4',gdrv_id)
        if Trnl.sh2.acell('W2').value == 'manual':
            methods(bot,update)
        elif Trnl.sh2.acell('W2').value == 'auto':
            if 'method=PLM' in Trnl.sh2.acell('W3').value:
                plhh_method(bot, update)
            elif 'method=TM' in Trnl.sh2.acell('W3').value:
                transload_method(bot, update)
            elif 'method=DM' in Trnl.sh2.acell('W3').value:
                direct_method(bot, update)
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
@pyrogram.Client.on_message(pyrogram.filters.command(["cnmm"]))
def cnmm_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        mv_kw = update.reply_to_message.text
        cnmm_lst = channelmyanmar(mv_kw)
        bot.send_message(
            chat_id=update.chat.id,
            text="တွေ့ရှိသည်များ 👇"
        )
        for c in cnmm_lst:
            bot.send_message(
                chat_id=update.chat.id,
                text=c
            )
        bot.send_message(
            chat_id=update.chat.id,
            text="အဖြစ်နိုင်ဆုံး 👇\n" + cnmm_lst[0]
        )
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
@pyrogram.Client.on_message(pyrogram.filters.command(["poster"]))
def poster_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        vlink = Trnl.sh2.acell('C2').value
        thumb_poster = Config.DOWNLOAD_LOCATION + "/1700943365/" + os.path.splitext(vlink.split('/')[-1])[0] + '.jpeg'
        width = Trnl.sh2.acell('C5').value
        height = Trnl.sh2.acell('C6').value
        fdmn_frame(vlink,thumb_poster,width,height)
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )        
@pyrogram.Client.on_message(pyrogram.filters.command(["srvk1"]))
async def srs_invt_rvk(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        srs_chnl_id_lst = Trnl.sh3.col_values(6)
        srs_chnl_invt_lk_lst = Trnl.sh3.col_values(2)
        srs_chnl_id_lst.pop(0)
        srs_chnl_invt_lk_lst.pop(0)
        for id in srs_chnl_id_lst:
            try:
                index = srs_chnl_id_lst.index(id)
                chnl = await bot.get_chat(chat_id=int(id))
                chnl_nm = chnl['title']
                chnl_invt_lk = srs_chnl_invt_lk_lst[int(index)]
                await bot.revoke_chat_invite_link(
                    chat_id = int(id),
                    invite_link = str(chnl_invt_lk)
                )
                await bot.send_message(
                    chat_id=update.chat.id,
                    text="<b>{}</b> movie channel မှ invite link <b>{}</b> ကို ပိတ်လိုက်ပါပြီ".format(chnl_nm, chnl_invt_lk)
                )
            except:
                pass
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )          
@pyrogram.Client.on_message(pyrogram.filters.command(["cmd"]))
def command_tool(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        if update.reply_to_message.text is not None:
            cmd_txt = update.reply_to_message.text
            cmd_lst = cmd_txt.split(' ')
            process = subprocess.Popen(cmd_lst, stdout=subprocess.PIPE,encoding="utf-8",universal_newlines=False)
            while process.poll() is None:
                nline = process.stdout.readline().rstrip()
                try:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=str(nline)
                    )
                except:
                    pass
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )                  
@pyrogram.Client.on_message(pyrogram.filters.command(["tmupd2"]))
async def fdmn_countdown(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
        promo_txt = Trnl.sh5.acell('I2').value
        promo_prd = Trnl.sh5.acell('J2').value
        promo_fee = Trnl.sh5.acell('K2').value
        time_info = Trnl.sh5.acell('L2').value
        promo_mssg_id = int(Trnl.sh5.acell('M2').value)
        if '-' in time_info:
            year,month,day,hour,minute,second = int(time_info.split('-')[0]),int(time_info.split('-')[1]),int(time_info.split('-')[2]),int(time_info.split('-')[3]),int(time_info.split('-')[4]),int(time_info.split('-')[5])
            future = datetime(year,month,day,hour,minute,second)
            present = datetime.now()
            t = (future - present).total_seconds()
        elif '-' not in time_info:
            t = int(time_info)
        #while t:
        timer = convert(t)
        await bot.edit_message_text(
            chat_id='@fdmnchannel',
            message_id=promo_mssg_id,
            text=promo_txt.format(timer, promo_fee, promo_prd, promo_fee)
        )
            #time.sleep(3600)
            #t -= 3600
    elif update.from_user.id not in Config.AUTH_USERS:
        bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id
        )
