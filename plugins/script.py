import logging
import os
import requests
import io

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation
from channels import channels
import pyrogram
from pyrogram.types.bots_and_keyboards import InlineKeyboardButton, InlineKeyboardMarkup

logging.getLogger("pyrogram").setLevel(logging.WARNING)
from trnl import Trnl
@pyrogram.Client.on_message(pyrogram.filters.command(["scpt"]))
async def script_call_back(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        script_url = Trnl.sh2.acell('M2').value
        phto_url = Trnl.sh2.acell('C2').value
        #r = requests.get(phto_url)
        #phto_bio = io.BytesIO(r.content)
        msg_trm = Trnl.sh2.acell('O2').value
        vcap = Trnl.sh2.acell('D2').value
        scpt_msg = await bot.send_message(
            chat_id="@fdmnscripts",
            text=msg_trm,
            parse_mode = 'html'
        )
        scpt_id = scpt_msg.message_id
        vtext_lk = "https://t.me/fdmnscripts/" + str(scpt_id)
        vtext_hplk = '<a href="' + vtext_lk + '">👉 ဇာတ်ညွှန်းဖတ်ရန် နှိပ်ပါ 📜</a>'
        typ = Trnl.sh2.acell('P3').value
        if "Movie" in typ:
            chnl_lk = str(Trnl.sh2.acell('I2').value)
            vd_lk = chnl_lk + str(Trnl.sh2.acell('P2').value)
            if Trnl.sh2.acell('J2').value == channels.gn_chnl[0]:
                invt_lk = channels.gn_chnl[2]
            elif Trnl.sh2.acell('J2').value == channels.bt_chnl[0]:
                invt_lk = channels.bt_chnl[2]
            elif Trnl.sh2.acell('J2').value == channels.ani_chnl[0]:
                invt_lk = channels.ani_chnl[2]
            elif Trnl.sh2.acell('J2').value == channels.rt_chnl[0]:
                invt_lk = channels.rt_chnl[2]
        invt_lk = 'https://t.me/FDMN_Signup_Bot'
        if "Series" in typ:
            invt_lk = Trnl.sh2.acell('I2').value
            vd_lk = invt_lk
        vd_hplk = '<a href="' + vd_lk + '">👉 ဇာတ်လမ်းကြည့်ရန် နှိပ်ပါ 🍿</a>'
        chnl_hplk = '<a href="' + invt_lk + '">👉 Channel Join ရန်နှိပ်ပါ 🔗</a>'
        vd_qlt = Trnl.sh2.acell('H2').value
        mv_gnr = Trnl.sh2.acell('M3').value
        rntm = Trnl.sh2.acell('M4').value
        year = Trnl.sh2.acell('M5').value
        ctry = Trnl.sh2.acell('M6').value
        imdb = Trnl.sh2.acell('M8').value
        vcap = '<b>' + vcap + '</b>'
        if "Movie" in typ:
            mssg = vcap + "\n\n⭐IMDB: " + imdb + "\n🎬 " + mv_gnr + "\n🗓️ " + year + " 🎞️ " + typ + " 📺 " + vd_qlt + "\n⏰ " + rntm + "\n🌎 " + ctry + "\n\n" + chnl_hplk + "\n\n" + vtext_hplk + "\n\n" + vd_hplk + "\n\n" + Translation.CHNL_JOIN
        if "Series" in typ:
            mssg = vcap + "\n\n⭐IMDB: " + imdb + "\n🎬 " + mv_gnr + "\n🗓️ " + year + " 🎞️ " + typ + " 📺 " + vd_qlt + "\n⏰ " + rntm + "\n🌎 " + ctry + "\n\n" + vtext_hplk + "\n\n" + vd_hplk + "\n\n" + Translation.CHNL_FB
        try:
            mchnl_msg = await bot.send_photo(
                "@fdmnchannel",
                phto_url,
                mssg,
                'html'
            )
        except:
            phto_req = requests.get(phto_url)
            phto_bio = io.BytesIO(phto_req.content)
            mchnl_msg = await bot.send_photo(
                "@fdmnchannel",
                phto_bio,
                mssg,
                'html'
            )
        Trnl.sh2.update('G2', mchnl_msg.message_id)
        await bot.send_message(
            chat_id=update.chat.id,
            text="Post တင်လိုက်သော ဇာတ်လမ်း 👇\n" + script_url
        )
