import pyrogram
from pyrogram.types import InputMediaPhoto
from trnl import Trnl
import logging
import requests
import io
from googletrans import Translator
from plugins.func_scpt import func_scpt

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pyrogram.Client.on_message(pyrogram.filters.command(["stp2"]))
def setup(bot, update):
    full_id = update.chat.id
    Trnl.sh2.update('J2',full_id)
    Trnl.sh2.update('P3','Series')
    #invt_lk = bot.create_chat_invite_link(chat_id=update.chat.id)
    chat = bot.get_chat(chat_id=update.chat.id)
    Trnl.sh2.update('I2',chat['invite_link'])
    bot.delete_messages(
        chat_id=full_id,
        message_ids=update.message_id
    )
    r = requests.get(Trnl.sh2.acell('C2').value)
    inmemoryfile = io.BytesIO(r.content)
    bot.set_chat_photo(
        chat_id=full_id,
        photo=inmemoryfile
    )
    no_find = Trnl.sh3.col_values(1)
    no_lst = []
    for n in no_find:
        if n.isdigit():
            no_lst.append(n)
    try:
        base = int(max(no_lst))
        srs_no = "{0:0=3d}".format( base + 1)
        translator = Translator()
        srs_no = translator.translate(srs_no,'my','en').text
    except:
        srs_no = '၀၀၀'
    try:
        srs_no = srs_no.replace('း','')
    except:
        pass
    index = len(no_find)+1
    Trnl.sh3.update('A{}'.format(index),srs_no)
    Trnl.sh2.update('D3',srs_no)
    Trnl.sh3.update('B{}'.format(index),chat['invite_link'])
    Trnl.sh3.update('C{}'.format(index),chat['title'])
@pyrogram.Client.on_message(pyrogram.filters.command(["pic2"]))
def setpic(bot, update):
    r = requests.get(Trnl.sh2.acell('C2').value)
    inmemoryfile = io.BytesIO(r.content)
    bot.delete_messages(
        chat_id=update.chat.id,
        message_ids=update.message_id
    )
    bot.set_chat_photo(
        chat_id=update.chat.id,
        photo=inmemoryfile
    )
@pyrogram.Client.on_message(pyrogram.filters.command(["id2"]))
def sendid(bot, update):
    chat = bot.get_chat(chat_id=update.chat.id)
    full_id = update.chat.id
    srs_name = chat['title']
    srs_row = Trnl.sh3.findall(srs_name)[0].row
    Trnl.sh3.update('D{}'.format(srs_row),'ပြသဆဲ...')
    Trnl.sh2.update('J2',full_id)
    Trnl.sh2.update('P3','Series')
    bot.delete_messages(
        chat_id=full_id,
        message_ids=update.message_id
    )
@pyrogram.Client.on_message(pyrogram.filters.command(["ad2"]))
def audio(bot, update):
    full_id = update.chat.id
    aud_ext = update.text.split(' ')[1]
    Trnl.sh2.update('E3',aud_ext)
    bot.delete_messages(
        chat_id=full_id,
        message_ids=update.message_id    
    )
@pyrogram.Client.on_message(pyrogram.filters.command(["ed2"]))
def finish(bot, update):
    chat = bot.get_chat(chat_id=update.chat.id)
    srs_name = chat['title']
    srs_row = Trnl.sh3.findall(srs_name)[0].row
    Trnl.sh3.update('D{}'.format(srs_row),'ဇာတ်သိမ်းပြီး...')
    text = "{} ဇာတ်လမ်းတွဲ တင်ဆက်မှု ဒီမှာပဲ ပြီးဆုံးသွားပါပြီ 🔚\n\nတခြားသောဇာတ်လမ်းတွေကို 👉<a href='https://www.facebook.com/fdmntelegram'>FDMN Facebook Page</a>👈 နဲ့ 👉<a href='https://t.me/fdmnchannel'>FDMN Telegram Channel</a>👈 တို့ကနေ စောင့်ကြည့်နိုင်ပါတယ်။\n\nကြည့်ရှုအားပေးတဲ့သူအားလုံးနဲ့ ဘာသာပြန်တင်ဆက်ပေးတဲ့ မူရင်း source အားလုံးကို FDMN Channel မှ ကျေးဇူးတင်ရှိပါတယ်...".format(chat['title'])
    bot.delete_messages(
        chat_id=update.chat.id,
        message_ids=update.message_id    
    )
    bot.send_message(
        chat_id=update.chat.id,
        text=text,
        parse_mode="html",
        disable_web_page_preview=True
    )
