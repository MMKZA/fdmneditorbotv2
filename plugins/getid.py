import pyrogram
from trnl import Trnl

@pyrogram.Client.on_message(pyrogram.filters.command(["hi2"]))
def getid2(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        full_id = update.chat.id
        invt_lk = bot.export_chat_invite_link(chat_id=full_id)
        invt_1st = invt_lk.split('/',1)[0] + "/"
        invt_2nd = invt_lk.split('/',1)[1]
        Trnl.sh2.update('J2',full_id)
        Trnl.sh2.update('I2',invt_1st)
        Trnl.sh2.update('P2',invt_2nd)
        bot.delete_messages(
            chat_id=full_id,
            message_ids=update.message_id
        )
