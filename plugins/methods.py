import pyrogram
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from trnl import Trnl
import asyncio
from plugins.gdrvclean import gdrvclean
from plugins.transloader import transloader
from plugins.echo_echo import echo_echo
from plugins.plhh_gdrive import plhh_gdrive
import os
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
import requests
from bs4 import BeautifulSoup

#import logging
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logger = logging.getLogger(__name__)

def methods(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Public Link Method", callback_data="method=PLM")],
                [InlineKeyboardButton("Transload Method", callback_data="method=TM")],
                [InlineKeyboardButton("Direct Method", callback_data="method=DM")],
            ]
        )
        bot.send_message(
            chat_id=update.from_user.id,
            text="Method ရွေးပါ 👇",
            reply_markup=reply_markup,
            parse_mode="html",
        )
def transload_method(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        gdrv_id = Trnl.sh2.acell('L4').value
        gdrv_lk = 'https://drive.google.com/file/d/{}/view?usp=sharing'.format(gdrv_id)
        #logger.info(gdrv_lk)
        base = Trnl.sh2.acell('K2').value
        final_link = transloader(base, gdrv_lk)
        #logger.info(final_link)
        Trnl.sh2.update('L2', final_link)
        arc_kw = ['.zip','.rar','.7z']
        vd_kw = ['.mp4','.mkv','.mov','.m4v']
        fl_ext = os.path.splitext(final_link)[1]
        if fl_ext in arc_kw:
            text = "Archive ဖိုင်အမျိုးအစားဖြစ်ပါတယ်၊ 🗃️SFile ကိုရွေးချယ်ပါ 👇\n"
            mssg = bot.send_message(
                chat_id=update.from_user.id,
                text=text + final_link
            )
        elif fl_ext in vd_kw:
            text = "Video ဖိုင်အမျိုးအစားဖြစ်ပါတယ်၊ 📺SVideo ကိုရွေးချယ်ပါ 👇\n"
            mssg = bot.send_message(
                chat_id=update.from_user.id,
                text=text + final_link
            )
        else:
            text = "Link အမှားအယွင်းရှိနိုင်ပါတယ်၊ သေချာစစ်ကြည့်ပါ ⚠️\n"
            mssg = bot.send_message(
                chat_id=update.from_user.id,
                text=text + final_link
            )
        echo_echo(bot,update,final_link,mssg,mssg.message_id)
def plhh_method(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        gdrv_id = Trnl.sh2.acell('L4').value
        gdrv_lk = 'https://drive.google.com/file/d/{}/view?usp=sharing'.format(gdrv_id)
        req = requests.get(gdrv_lk)
        soup = BeautifulSoup(req.content, 'lxml')
        for s in soup.select('head > title'):
            gdrv_fl_fll_nm = s.text.split(' - ')[0]
        ytsn_fl_fll_nm = Trnl.sh2.acell('D6').value
        vd_kw = ['.mkv','.m4a','.mov','.avi']
        arc_kw = ['.zip','.rar','.7z']
        if gdrv_fl_fll_nm not in ytsn_fl_fll_nm:
            vd_ext = os.path.splitext(gdrv_fl_fll_nm)[1]
            if vd_ext != '' and vd_ext in vd_kw and vd_ext not in arc_kw:
                fl_fll_nm = gdrv_fl_fll_nm.replace(vd_ext,'.mp4')
                Trnl.sh2.update('D6',fl_fll_nm)
        elif gdrv_fl_fll_nm in ytsn_fl_fll_nm:
            vd_ext = os.path.splitext(ytsn_fl_fll_nm)[1]
            if vd_ext != '' and vd_ext in vd_kw and vd_ext not in arc_kw:
                fl_fll_nm = ytsn_fl_fll_nm.replace(vd_ext,'.mp4')
                Trnl.sh2.update('D6',fl_fll_nm)
        del req
        final_link = plhh_gdrive(gdrv_lk)
        Trnl.sh2.update('L2', final_link)
        if 'https://api.a-u.workers.dev/download/' in final_link:
            text = "📺SVideo or 🗃️SFile မှန်ရာကိုရွေးချယ်ပါ 👇\n"
            mssg = bot.send_message(
                chat_id=update.from_user.id,
                text=text + final_link
            )
        echo_echo(bot,update,final_link,mssg,mssg.message_id)
            
def direct_method(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        gdrv_id = Trnl.sh2.acell('L4').value
        gdrv_lk = 'https://drive.google.com/file/d/{}/view?usp=sharing'.format(gdrv_id)
        req = requests.get(gdrv_lk)
        soup = BeautifulSoup(req.content, 'lxml')
        for s in soup.select('head > title'):
            gdrv_fl_fll_nm = s.text.split(' - ')[0]
        ytsn_fl_fll_nm = Trnl.sh2.acell('D6').value
        vd_kw = ['.mkv','.m4a','.mov','.avi']
        arc_kw = ['.zip','.rar','.7z']
        if gdrv_fl_fll_nm not in ytsn_fl_fll_nm:
            vd_ext = os.path.splitext(gdrv_fl_fll_nm)[1]
            if vd_ext != '' and vd_ext in vd_kw and vd_ext not in arc_kw:
                fl_fll_nm = gdrv_fl_fll_nm.replace(vd_ext,'.mp4')
                Trnl.sh2.update('D6',fl_fll_nm)
        elif gdrv_fl_fll_nm in ytsn_fl_fll_nm:
            vd_ext = os.path.splitext(ytsn_fl_fll_nm)[1]
            if vd_ext != '' and vd_ext in vd_kw and vd_ext not in arc_kw:
                fl_fll_nm = ytsn_fl_fll_nm.replace(vd_ext,'.mp4')
                Trnl.sh2.update('D6',fl_fll_nm)
        del req
        final_link = gdrv_lk
        Trnl.sh2.update('L2', final_link)
        text = "📺SVideo or 🗃️SFile မှန်ရာကိုရွေးချယ်ပါ 👇\n"
        mssg = bot.send_message(
            chat_id=update.from_user.id,
            text=text + final_link
        )
        echo_echo(bot,update,final_link,mssg,mssg.message_id)
