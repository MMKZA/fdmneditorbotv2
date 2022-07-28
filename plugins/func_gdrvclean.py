import pyrogram
from plugins.gdrvclean import gdrvclean

@pyrogram.Client.on_message(pyrogram.filters.command(["cl2"]))
def clean(bot, update):
    status = "error"
    gdrvclean(status)
    bot.delete_messages(
        chat_id=update.chat.id,
        message_ids=update.message_id
    )
