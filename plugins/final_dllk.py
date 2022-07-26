from config import Config
import pyrogram
from plugins.gldchnl import gldchnl
from plugins.cnmm import cnmm
import logging
from trnl import Trnl
from plugins.ytsn_dllk import ytsn_dllk
from plugins.gdrvclean import gdrvclean
from plugins.transloader import transloader
from plugins.func_scpt import func_scpt
from plugins.series import series
import os
import re
import time

@pyrogram.Client.on_message(pyrogram.filters.regex(pattern=".*http.*"))
def trans(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        if "/srs" in update.text:
            web_url = update.text.split(' ', 1)[1]
            Trnl.sh2.update('M2', web_url)
            func_scpt(web_url)
            epsd_msg = series(web_url)
            bot.send_message(
                chat_id=update.chat.id,
                text=epsd_msg[0]
            )
            bot.send_message(
                chat_id=update.chat.id,
                text=epsd_msg[1]
            )
            bot.send_message(
                chat_id=update.chat.id,
                text=epsd_msg[2]
            )
        if "/srs" not in update.text:
            web_url = update.text
            Trnl.sh2.update('M2',web_url)
            if "https://goldchannel.net/movies/" in web_url:
                gdrv_lk = gldchnl(web_url)
                func_scpt(web_url)
                avlb_lk = Trnl.sh2.acell('Q2').value
                bot.send_message(
                    chat_id=update.chat.id,
                    text="ရရှိနိုင်သော links များ👇\n" + avlb_lk
                )
                base = Trnl.sh1.acell('K2').value
                final_link = transloader(base,gdrv_lk)
                Trnl.sh2.update('L2', final_link)
                bot.send_message(
                    chat_id=update.chat.id,
                    text="Link မှန်ကန်ပါက ဇာတ်ကားတင်လို့ရပါပြီ 👇\n" + final_link
                )
            if "https://channelmyanmar.org/" in web_url:
                ytsn_lk = cnmm(web_url)
                func_scpt(web_url)
                avlb_lk = Trnl.sh2.acell('Q2').value
                bot.send_message(
                    chat_id=update.chat.id,
                    text="ရရှိနိုင်သော links များ👇\n" + avlb_lk
                )
                gdrv_retrn = ytsn_dllk(ytsn_lk)
                if "error" in gdrv_retrn:
                    gdrvclean(gdrv_retrn)
                    gdrv_lk = ytsn_dllk(ytsn_lk)
                else:
                    gdrv_lk = gdrv_retrn
                #bot.send_message(
                    #chat_id=update.chat.id,
                    #text=gdrv_lk
                #)
                base = Trnl.sh1.acell('K2').value
                final_link = transloader(base,gdrv_lk)
                Trnl.sh2.update('L2', final_link)
                bot.send_message(
                    chat_id=update.chat.id,
                    text="Link မှန်ကန်ပါက ဇာတ်ကားတင်လို့ရပါပြီ 👇\n" + final_link
                )
