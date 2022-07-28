import pyrogram
from trnl import Trnl

@pyrogram.Client.on_message(pyrogram.filters.command(["hi2"]))
def getid2(bot, update):
    full_id = update.chat.id
    invt_lk = bot.export_chat_invite_link(chat_id=full_id)
    Trnl.sh2.update('J2',full_id)
    Trnl.sh2.update('I2',invt_lk)
    bot.delete_messages(
        chat_id=full_id,
        message_ids=update.message_id
    )
