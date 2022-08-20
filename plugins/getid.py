import pyrogram
from pyrogram.types import InputMediaPhoto
from trnl import Trnl
import logging
import requests
import io
from googletrans import Translator

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
    full_id = update.chat.id
    Trnl.sh2.update('J2',full_id)
    Trnl.sh2.update('P3','Series')
    bot.delete_messages(
        chat_id=full_id,
        message_ids=update.message_id
    )
@pyrogram.Client.on_message(pyrogram.filters.command(["im2"]))
def imdb(bot, update):
    full_id = update.chat.id
    imdb_id = update.text.split(' ')[1]
    Trnl.sh2.update('M7',imdb_id)
    bot.delete_messages(
        chat_id=full_id,
        message_ids=update.message_id
    )
