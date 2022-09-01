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
from plugins.blc import blc
from plugins.bs import bs
from plugins.shweflix import shweflix
from plugins.echo_auto import echo_auto
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import re
import time
import asyncio
from googletrans import Translator
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pyrogram.Client.on_message(pyrogram.filters.regex(pattern=".*http.*"))
def final_dllk(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        base = Trnl.sh2.acell('K2').value
        web_url = update.text
        
        srs_kw_lst = ['tvshows']
        act_srs_kw = ''
        for srs_kw in srs_kw_lst:
            if srs_kw in web_url:
                act_srs_kw = srs_kw
                
        source_kw_lst = ['https://channelmyanmar.org/','https://goldchannel.net/','https://shweflix.org/']
        act_source_kw = ''
        for source_kw in source_kw_lst:
            if source_kw in web_url:
                act_source_kw = source_kw
        
        trsl_kw_lst = ['https://yoteshinportal.cc/','https://drive.google.com/']
        act_trsl_kw = ''
        for trsl_kw in trsl_kw_lst:
            if trsl_kw in web_url:
                act_trsl_kw = trsl_kw
                
        imdb_kw_lst = ['https://www.imdb.com/title/tt','https://m.imdb.com/title/tt']
        act_imdb_kw = ''
        for imdb_kw in imdb_kw_lst:
            if imdb_kw in web_url:
                act_imdb_kw = imdb_kw
                
        if (act_source_kw in web_url) and (act_srs_kw != '') and (act_srs_kw in web_url) and (act_imdb_kw == '') and (act_trsl_kw == '') and ('https://t.me/c' not in web_url):
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
                if len(epsd_lst) == 3:
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
                if len(epsd_lst) == 2:
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

        if (act_source_kw in web_url) and (act_srs_kw == '') and (act_imdb_kw == '') and (act_trsl_kw == '') and ('https://t.me/c' not in web_url):
            Trnl.sh2.update('M2', web_url)
            Trnl.sh2.update('P3', "Movie")
            if "https://shweflix.org/" in web_url:
                func_scpt(web_url)
                rtrn = shweflix(web_url)
                bot.send_message(
                    chat_id=update.chat.id,
                    text="Links အားလုံး👇\n" + rtrn[0]
                )
                bot.send_message(
                    chat_id=update.chat.id,
                    text="Size အကြီးဆုံး Link👇\n" + rtrn[1]
                )
            if "https://burmesesubtitles.com/" in web_url:
                func_scpt(web_url)
                if web_url in Trnl.sh2.acell('L3').value:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=Trnl.sh2.acell('L3').value
                    )
                bs_rtrn = bs(web_url)
                avlb_lk = Trnl.sh2.acell('Q2').value
                if len(bs_rtrn) == 1:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="Links အားလုံး👇\n" + avlb_lk
                    )
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="Size အကြီးဆုံး Links များ 👇\n" + bs_rtrn[0]
                    )
                if len(bs_rtrn) == 2:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="Links အားလုံး👇\n" + avlb_lk
                    )
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="Size အကြီးဆုံး Links များ 👇\n" + bs_rtrn[0]
                    )
                    gdrv_lk = bs_rtrn[1]
                    final_link = transloader(base, gdrv_lk)
                    Trnl.sh2.update('L2', final_link)
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="Link မှန်ကန်ပါက ဇာတ်ကားတင်လို့ရပါပြီ 👇\n" + final_link
                    )
            if "burmalinkchannel" in web_url:
                func_scpt(web_url)
                if web_url in Trnl.sh2.acell('L3').value:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=Trnl.sh2.acell('L3').value
                    )
                ytsn_lk = blc(web_url)
                if "Manual" in ytsn_lk:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=ytsn_lk
                    )
                if "Manual" not in ytsn_lk:
                    avlb_lk = Trnl.sh2.acell('Q2').value
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="ရရှိနိုင်သော links များ👇\n" + avlb_lk
                    )
                    final_link = transloader(base, ytsn_lk)
                    Trnl.sh2.update('L2', final_link)
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="Link မှန်ကန်ပါက ဇာတ်ကားတင်လို့ရပါပြီ 👇\n" + final_link
                    )
            if "https://goldchannel.net/" in web_url:
                func_scpt(web_url)
                if web_url in Trnl.sh2.acell('L3').value:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=Trnl.sh2.acell('L3').value
                    )
                gdrv_lst = gldchnl(web_url)
                if web_url in Trnl.sh2.acell('H3').value:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=Trnl.sh2.acell('H3').value
                    )
                avlb_lk = Trnl.sh2.acell('Q2').value
                bot.send_message(
                    chat_id=update.chat.id,
                    text="ရရှိနိုင်သော links များ👇\n" + avlb_lk
                )
                inline_keyboard = []
                for gdrv in gdrv_lst:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=gdrv,
                        disable_web_page_preview=True
                    )
                    if 'drive.google.com' in gdrv:
                        lk = gdrv.split('|')[0].strip()
                        lk = '{}|{}'.format(lk.split('/')[2],lk.split('/')[5])
                        qlt = gdrv.split('|')[1].strip()
                        sz = gdrv.split('|')[2].strip()
                        inline_keyboard.append([InlineKeyboardButton('Quality: {} ; Size: {}'.format(qlt,sz),callback_data=str(lk).encode("UTF-8"))])
                reply_markup = InlineKeyboardMarkup(inline_keyboard)
                try:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="တင်မယ့် Quality ရွေးပါ 👇",
                        reply_markup=reply_markup,
                        parse_mode="html",
                        reply_to_message_id=update.message_id
                    )
                except:
                    pass
                #final_link = transloader(base, gdrv_lk)
                #Trnl.sh2.update('L2', final_link)
                #bot.send_message(
                    #chat_id=update.chat.id,
                    #text="Link မှန်ကန်ပါက ဇာတ်ကားတင်လို့ရပါပြီ 👇\n" + final_link
                #)
                #asyncio.run(echo_auto(bot,update,final_link))
            if "https://channelmyanmar.org/" in web_url:
                func_scpt(web_url)
                if web_url in Trnl.sh2.acell('L3').value:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=Trnl.sh2.acell('L3').value
                    )
                cnmm_rtrn = cnmm(web_url)
                if len(cnmm_rtrn) == 1:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="အခက်အခဲဖြစ်ပေါ်နေလို့ Manual ရွေးပါ 👇"
                    )
                    for epsd in cnmm_rtrn[0]:
                        bot.send_message(
                            chat_id=update.chat.id,
                            text=epsd,
                            disable_web_page_preview=True
                        )
                if len(cnmm_rtrn) == 4:
                    max_lk = cnmm_rtrn[1]
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="ရရှိနိုင်သော Link အားလုံး 👇"
                    )
                    inline_keyboard = []
                    for epsd in cnmm_rtrn[0]:
                        bot.send_message(
                            chat_id=update.chat.id,
                            text=epsd,
                            disable_web_page_preview=True
                        )
                        if 'yoteshinportal.cc' in epsd:
                            lk = epsd.split('|')[0].strip()
                            qlt = epsd.split('|')[1].strip()
                            sz = epsd.split('|')[2].strip()
                            inline_keyboard.append([InlineKeyboardButton('Quality: {} ; Size: {}'.format(qlt,sz),callback_data=str(lk).encode("UTF-8"))])
                    reply_markup = InlineKeyboardMarkup(inline_keyboard)
                    if len(inline_keyboard) != 0:
                        bot.send_message(
                            chat_id=update.chat.id,
                            text="တင်မယ့် Quality ရွေးပါ 👇",
                            reply_markup=reply_markup,
                            parse_mode="html",
                            reply_to_message_id=update.message_id
                        )
                    #bot.send_message(
                        #chat_id=update.chat.id,
                        #text="2 GB ထက်နည်းသော Link - Quality: {} - Size: {} GB👇\n{}".format(cnmm_rtrn[2],cnmm_rtrn[3],max_lk),
                        #disable_web_page_preview=True
                    #)
                    #gdrv_retrn = ytsn_dllk(max_lk)
                    #if "error" in gdrv_retrn:
                        #gdrvclean(gdrv_retrn)
                        #gdrv_lk = ytsn_dllk(max_lk)
                    #else:
                        #gdrv_lk = gdrv_retrn
                    #final_link = transloader(base, gdrv_lk)
                    #Trnl.sh2.update('L2', final_link)
                    #arc_kw = ['.zip','.rar','.7z']
                    #vd_kw = ['.mp4','.mkv','.mov','.m4v']
                    #fl_ext = os.path.splitext(final_link)[1]
                    #if fl_ext in arc_kw:
                        #text = "Archive ဖိုင်အမျိုးအစားဖြစ်ပါတယ်၊ 🗃️SFile ကိုရွေးချယ်ပါ 👇\n"
                        #bot.send_message(
                            #chat_id=update.chat.id,
                            #text=text + final_link
                        #)
                        #asyncio.run(echo_auto(bot,update,final_link))
                    #elif fl_ext in vd_kw:
                        #text = "Video ဖိုင်အမျိုးအစားဖြစ်ပါတယ်၊ 📺SVideo ကိုရွေးချယ်ပါ 👇\n"
                        #bot.send_message(
                            #chat_id=update.chat.id,
                            #text=text + final_link
                        #)
                        #asyncio.run(echo_auto(bot,update,final_link))
                    #else:
                        #text = "Link အမှားအယွင်းရှိနိုင်ပါတယ်၊ သေချာစစ်ကြည့်ပါ ⚠️\n"
                        #bot.send_message(
                            #chat_id=update.chat.id,
                            #text=text + final_link
                        #)
        if (act_imdb_kw != '') and (act_imdb_kw in web_url) and ('https://t.me/c' not in web_url):
            imdb_lk = web_url
            try:
                imdb_id = imdb_lk.split('/')[-2]
            except:
                imdb_id = imdb_lk
            Trnl.sh2.update('M7',imdb_id)
            script_url = Trnl.sh2.acell('M2').value
            func_scpt(script_url)
            bot.delete_messages(
                chat_id=update.chat.id,
                message_ids=update.message_id
            )
        if (act_trsl_kw != '') and (act_trsl_kw in web_url) and ('https://t.me/c' not in web_url):
            if '|' in web_url:
                lk = web_url.split("|")[0].strip()
            else:
                lk = web_url
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
                
        if 'https://t.me/c' in web_url:
            vd_id = web_url.split("/")[-1]
            Trnl.sh2.update('P2',vd_id)
            bot.delete_messages(
                chat_id=update.chat.id,
                message_ids=update.message_id
            )
