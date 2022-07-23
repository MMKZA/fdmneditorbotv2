from config import Config
import pyrogram
from plugins.gldchnl import gldchnl
from plugins.cnmm import cnmm
import logging
from trnl import Trnl
from plugins.ytsn_dllk import ytsn_dllk
from plugins.transloader import transloader
import os
import re

@pyrogram.Client.on_message(pyrogram.filters.regex(pattern=".*http.*"))
def trans(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        web_url = update.text
        Trnl.sh1.update('M3',web_url)
        if "https://goldchannel.net/movies/" in web_url:
            gdrv_lk = gldchnl(web_url)
            #await bot.send_message(
                #chat_id=update.chat.id,
                #text=gdrv_lk
            #)
            base = Trnl.sh1.acell('K2').value
            final_link = transloader(base,gdrv_lk)
            Trnl.sh1.update('L3', final_link)
            bot.send_message(
                chat_id=update.chat.id,
                text="Link မှန်ကန်ပါက ဇာတ်ကားတင်လို့ရပါပြီ 👇\n" + final_link
            )
        if "https://channelmyanmar.org/" in web_url:
            ytsn_lk = cnmm(web_url)
            gdrv_retrn = ytsn_dllk(ytsn_lk)
            if "error" in gdrv_retrn:
                gdrvclean(gdrv_retrn)
                gdrv_lk = ytsn_dllk(ytsn_lk)
            else:
                gdrv_lk = gdrv_retrn
            #await bot.send_message(
                #chat_id=update.chat.id,
                #text=gdrv_lk
            #)
            base = Trnl.sh1.acell('K2').value
            final_link = transloader(base,gdrv_lk)
            Trnl.sh1.update('L3', final_link)
            bot.send_message(
                chat_id=update.chat.id,
                text="Link မှန်ကန်ပါက ဇာတ်ကားတင်လို့ရပါပြီ 👇\n" + final_link
            )
