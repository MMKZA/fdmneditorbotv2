from config import Config
import pyrogram
from plugins.gldchnl import gldchnl
from plugins.cnmm import cnmm
import logging
from trnl import Trnl
from plugins.ytsn_dllk import ytsn_dllk
from plugins.gdrvclean import gdrvclean
from plugins.func_scpt import func_scpt
from plugins.series import series
from plugins.blc import blc
from plugins.bs import bs
from plugins.shweflix import shweflix
from plugins.echo_auto import echo_auto
from plugins.echo_echo import echo_echo
from plugins.methods import methods
from plugins.imdb_info import imdb_info
from plugins.methods import methods,plhh_method,transload_method,direct_method
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.transloader import transloader
import os
import re
import time
import asyncio
from googletrans import Translator
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from plugins.file_download import file_upload

@pyrogram.Client.on_message(pyrogram.filters.regex(pattern=".*http.*"))
def final_dllk(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        base = Trnl.sh2.acell('K2').value
        if update.reply_to_message is not None:
            web_url_text = update.reply_to_message.text
        elif update.reply_to_message is None:
            web_url_text = update.text
        try:
            web_url = re.search("(?P<url>https?://[^\s]+)", web_url_text).group("url")
        except:
            web_url = web_url_text

        srs_kw_lst = ['tvshows']
        act_srs_kw = ''
        for srs_kw in srs_kw_lst:
            if srs_kw in web_url:
                act_srs_kw = srs_kw
                
        source_kw_lst = ['https://channelmyanmar.org/','https://goldchannel.net/','https://shweflix.org/','https://old.burmesesubtitles.com','https://burmesesubtitles.com']
        act_source_kw = ''
        for source_kw in source_kw_lst:
            if source_kw in web_url:
                act_source_kw = source_kw
        
        trsl_kw_lst = ['https://yoteshinportal.cc/','https://drive.google.com/','rapidleech.gq','megaup.net','workers.dev']
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
                all_lst = shweflix(web_url)
                bot.send_message(
                    chat_id=update.chat.id,
                    text="Links အားလုံး👇"
                )
                inline_keyboard = []
                all_lst_txt = '\n'.join(all_lst)
                Trnl.sh2.update('A6',all_lst_txt)
                for al in all_lst:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text=al,
                        disable_web_page_preview=True
                    )
                    index = all_lst.index(al)
                    qlt = al.split('|')[1].strip()
                    sz = al.split('|')[2].strip()
                    inline_keyboard.append([InlineKeyboardButton('Quality: {} ; Size: {}'.format(qlt,sz),callback_data='gdtot|{}'.format(index))])
                reply_markup = InlineKeyboardMarkup(inline_keyboard)
                if len(inline_keyboard) != 0:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="တင်မယ့် Quality ရွေးပါ 👇",
                        reply_markup=reply_markup,
                        parse_mode="html",
                        reply_to_message_id=update.message_id
                    )
            if "burmesesubtitles.com" in web_url:
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
                        text="Links အားလုံး👇\n"
                    )
                    for lk in bs_rtrn[0]:
                        bot.send_message(
                            chat_id=update.chat.id,
                            text=lk
                        )
                if len(bs_rtrn) == 2:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="Links အားလုံး👇\n"
                    )
                    for lk in bs_rtrn[0]:
                        bot.send_message(
                            chat_id=update.chat.id,
                            text=lk
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
                all_lst = gldchnl(web_url)
                all_lst_txt = "Links အားလုံး👇\n" + '\n'.join(all_lst)
                try:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text= all_lst_txt
                    )
                except:
                    pass
                inline_keyboard = []
                for al in all_lst:
                    lk = al.split('|')[0].strip()
                    qlt = al.split('|')[1].strip()
                    sz = al.split('|')[2].strip()
                    inline_keyboard.append([InlineKeyboardButton('Quality: {} ; Size: {}'.format(qlt,sz),callback_data=str(lk))])
                reply_markup = InlineKeyboardMarkup(inline_keyboard)
                if len(inline_keyboard) != 0:
                    bot.send_message(
                        chat_id=update.chat.id,
                        text="တင်မယ့် Quality ရွေးပါ 👇",
                        reply_markup=reply_markup,
                        parse_mode="html",
                        reply_to_message_id=update.message_id
                    )
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
                    ytsn_lst = []
                    for epsd in cnmm_rtrn[0]:
                        bot.send_message(
                            chat_id=update.chat.id,
                            text=epsd,
                            disable_web_page_preview=True
                        )
                        if 'yoteshinportal.cc' in epsd:
                            ytsn_lst.append(epsd)
                            lk = 'yoteshinportal.cc|{}'.format(cnmm_rtrn[0].index(epsd))
                            qlt = epsd.split('|')[1].strip()
                            sz = epsd.split('|')[2].strip()
                            inline_keyboard.append([InlineKeyboardButton('Quality: {} ; Size: {}'.format(qlt,sz),callback_data=str(lk).encode("UTF-8"))])
                    reply_markup = InlineKeyboardMarkup(inline_keyboard)
                    ytsn_lst_txt = '\n'.join([ytsn for ytsn in ytsn_lst])
                    Trnl.sh2.update('A6',ytsn_lst_txt)
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
                imdb_id = imdb_lk.split('/')[4]
            except:
                imdb_id = imdb_lk
            #Trnl.sh2.update('N7','open')
            Trnl.sh2.update('M7',imdb_id)
            movie_id = str(imdb_id).replace('tt','')
            imdb_info(movie_id)
            bot.delete_messages(
                chat_id=update.chat.id,
                message_ids=update.message_id
            )
        if (act_trsl_kw != '') and (act_trsl_kw in web_url) and ('https://t.me/c' not in web_url):
            if '|' in web_url:
                lk = web_url.split("|")[0].strip()
            else:
                lk = web_url
            if 'megaup.net' not in lk:
                dlst_kwd_lst = ['rapidleech.gq','workers.dev']
                act_dlst_kw = ''
                for k in dlst_kwd_lst:
                    if k in lk:
                        act_dlst_kw = k
                if act_dlst_kw != '' and act_dlst_kw not in lk:
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
                    try:
                        gdrv_id = gdrv_lk.split('/')[5]
                    except:
                        gdrv_id = gdrv_lk.split('/')[3].split('=')[1]
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
                elif act_dlst_kw != '' and act_dlst_kw in lk:
                    if Trnl.sh2.acell('X3').value == 'open':
                        asyncio.run(file_upload(bot, update))
                    elif Trnl.sh2.acell('X3').value == 'close':
                        Trnl.sh2.update('L2',lk)
                        text = "📺SVideo or 🗃️SFile မှန်ရာကိုရွေးချယ်ပါ 👇\n"
                        mssg = bot.send_message(
                            chat_id=update.from_user.id,
                            text=text + lk
                        )
                        echo_echo(bot,update,lk,mssg,mssg.message_id)
            elif 'megaup.net' in lk and '?download_token=' in lk:
                fl_fll_nm = lk.split('/')[4].split('?download_token')[0]
                vd_kw = ['.mkv','.m4a','.mov','.avi']
                vd_ext = os.path.splitext(fl_fll_nm)[1]
                if vd_ext != '' and vd_ext in vd_kw:
                    fl_fll_nm = fl_fll_nm.replace(vd_ext,'.mp4')
                Trnl.sh2.update('D6',fl_fll_nm)
                base = Trnl.sh2.acell('K2').value
                final_link = transloader(base, lk)
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
                    bot.send_message(
                        chat_id=update.from_user.id,
                        text=text + final_link
                    )
                
        if 'https://t.me/c' in web_url:
            id_lst = web_url.split('/')
            vd_id = id_lst[-1]
            chnl_id = int('-100' + id_lst[4])
            id_lst.pop()
            chnl_lk = '/'.join(id_lst) + '/'
            Trnl.sh2.update('P2',vd_id)
            Trnl.sh2.update('J2',chnl_id)
            Trnl.sh2.update('I2',chnl_lk)
            bot.delete_messages(
                chat_id=update.chat.id,
                message_ids=update.message_id
            )
