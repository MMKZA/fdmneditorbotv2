import logging
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation
import pyrogram
from pyrogram.types.bots_and_keyboards import InlineKeyboardButton, InlineKeyboardMarkup

logging.getLogger("pyrogram").setLevel(logging.WARNING)
from trnl import Trnl
@pyrogram.Client.on_message(pyrogram.filters.command(["scpt"]))
async def script_call_back(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        script_url = Trnl.sh2.acell('M2').value
        phto_url = Trnl.sh2.acell('C2').value
        msg_trm = Trnl.sh2.acell('O2').value
        vcap = Trnl.sh2.acell('D2').value
        scpt_msg = await bot.send_message(
            chat_id="@fdmnscripts",
            text=msg_trm,
            parse_mode='html'
        )
        scpt_id = scpt_msg.message_id
        vtext_lk = "https://t.me/fdmnscripts/" + str(scpt_id)
        vtext_hplk = '<a href="' + vtext_lk + '">👉 ဇာတ်ညွှန်းဖတ်ရန် နှိပ်ပါ 📜</a>'
        invt_lst = [
            "https://t.me/+RqwAss5VI6M0N2Rl",
            "https://t.me/+Hlpn-6_fi8c1OWI1",
            "https://t.me/+fYTgNiUsRaJlY2Y1",
            "https://t.me/+rg5dEnd2JgFiMTll"
        ]
        id_lst = [
            "-1001785695486",
            "-1001718578294",
            "-1001389311243",
            "-1001750623132"
        ]
        if Trnl.sh2.acell('J2').value == id_lst[0]:
          invt_lk = invt_lst[0]
        if Trnl.sh2.acell('J2').value == id_lst[1]:
          invt_lk = invt_lst[1]
        if Trnl.sh2.acell('J2').value == id_lst[2]:
          invt_lk = invt_lst[2]
        if Trnl.sh2.acell('J2').value == id_lst[3]:
          invt_lk = invt_lst[3]
        for id in id_lst:
            if Trnl.sh2.acell('J2').value != id:
                invt_lk = Trnl.sh2.acell('I2').value
                vd_lk = invt_lk
            else:
                chnl_lk = str(Trnl.sh2.acell('I2').value)
                vd_lk = chnl_lk + str(Trnl.sh2.acell('P2').value)
        vd_hplk = '<a href="' + vd_lk + '">👉 ဇာတ်လမ်းကြည့်ရန် နှိပ်ပါ 🍿</a>'
        chnl_hplk = '<a href="' + invt_lk + '">👉 Channel Join ရန်နှိပ်ပါ 🔗</a>'
        vd_qlt = Trnl.sh2.acell('H2').value
        mchnl_msg = await bot.send_photo(
            "@fdmnchannel",
            phto_url,
            "🎞️\n" + vcap + " | " + vd_qlt + "\n\n" + chnl_hplk + "\n\n" + vtext_hplk + "\n\n" + vd_hplk + "\n\n" + Translation.CHNL_JOIN,
            'html'
        )
        Trnl.sh2.update('G2', mchnl_msg.message_id)
        await bot.send_message(
            chat_id=update.chat.id,
            text="Post တင်လိုက်သော ဇာတ်လမ်း 👇\n" + script_url
        )
