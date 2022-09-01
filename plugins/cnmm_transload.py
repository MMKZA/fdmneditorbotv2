import pyrogram
from trnl import Trnl
import asyncio
from plugins.ytsn_dllk import ytsn_dllk
from plugins.gdrvclean import gdrvclean
from plugins.transloader import transloader
from plugins.echo_echo import echo_echo
import os
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def cnmm_transload(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        index = int(update.data.split('|')[1])
        ytsn_lst_txt = Trnl.sh2.acell('A6').value
        ytsn_lst = ytsn_lst_txt.split('\n')
        lk = ytsn_lst[index].split('|')[0].strip()
        logger.info(lk)
        gdrv_retrn = ytsn_dllk(lk)
        if "error" in gdrv_retrn:
            gdrvclean(gdrv_retrn)
            gdrv_lk = ytsn_dllk(lk)
        else:
            gdrv_lk = gdrv_retrn
        base = Trnl.sh2.acell('K2').value
        final_link = transloader(base, gdrv_lk)
        logger.info(final_link)
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
            echo_echo(bot,update,final_link,mssg,mssg.message_id)
        elif fl_ext in vd_kw:
            text = "Video ဖိုင်အမျိုးအစားဖြစ်ပါတယ်၊ 📺SVideo ကိုရွေးချယ်ပါ 👇\n"
            mssg = bot.send_message(
                chat_id=update.from_user.id,
                text=text + final_link
            )
            echo_echo(bot,update,final_link,mssg,mssg.message_id)
        else:
            text = "Link အမှားအယွင်းရှိနိုင်ပါတယ်၊ သေချာစစ်ကြည့်ပါ ⚠️\n"
            mssg = bot.send_message(
                chat_id=update.from_user.id,
                text=text + final_link
            )
