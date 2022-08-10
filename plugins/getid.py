import pyrogram
from pyrogram.types import InputMediaPhoto
from trnl import Trnl
import logging
import requests
import io

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pyrogram.Client.on_message(pyrogram.filters.command(["stp2"]))
def setup(bot, update):
    full_id = update.chat.id
    Trnl.sh2.update('J2',full_id)
    Trnl.sh2.update('P3','Series')
    invt_lk = bot.create_chat_invite_link(chat_id=update.chat.id)
    Trnl.sh2.update('I2',invt_lk['invite_link'])
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
def sendid(bot, update):
    full_id = update.chat.id
    imdb_id = update.message.split(' ')[1]
    Trnl.sh2.update('M7',imdb_id)
    bot.delete_messages(
        chat_id=full_id,
        message_ids=update.message_id
    )
