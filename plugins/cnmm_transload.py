import pyrogram
from trnl import Trnl
import asyncio
from plugins.ytsn_dllk import ytsn_dllk
from plugins.gdrvclean import gdrvclean
from plugins.transloader import transloader
from plugins.echo_auto import echo_auto
import os
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
    
async def cnmm_transload(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        lk = update.data
        if "yoteshinportal.cc" in lk:
            gdrv_retrn = ytsn_dllk(lk)
            if "error" in gdrv_retrn:
                gdrvclean(gdrv_retrn)
                gdrv_lk = ytsn_dllk(lk)
            else:
                gdrv_lk = gdrv_retrn
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
