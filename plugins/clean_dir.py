import pyrogram
import os
from pyrogram import Client
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config


async def scan_dir(dir_path):
    for f in os.scandir(dir_path):
        return f.path
    
@pyrogram.Client.on_message(pyrogram.filters.command(["dir"]))
async def get_list_dir(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
        if not os.path.exists(tmp_directory_for_each_user):
            lst_txt = "ဘာဖိုင်မှ မရှိပါ ⚠️"
            await bot.send_message(
                text=lst_txt,
                chat_id=update.chat.id
            )
        if os.path.exists(tmp_directory_for_each_user):
            fl_lst = []
            for subdir, dirs, files in os.walk(tmp_directory_for_each_user):
                for file in files:
                    filepath = subdir + os.sep + file
                    vd_kw = ['.mp4','.mkv','.m4v','.mov']
                    for vd in vd_kw:
                        if filepath.endswith(vd):
                            fl_lst.append(filepath)
            for fl in fl_lst:
                await bot.send_message(
                    text=fl,
                    chat_id=update.chat.id
                )
@pyrogram.Client.on_message(pyrogram.filters.command(["dirrm"]))
async def remove_dir(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
        if not os.path.exists(tmp_directory_for_each_user):
            lst_txt = "ဘာဖိုင်မှ မရှိပါ ⚠️"
            await bot.send_message(
                text=lst_txt,
                chat_id=update.chat.id
            )
        if os.path.exists(tmp_directory_for_each_user):
            fl_lst = []
            for subdir, dirs, files in os.walk(tmp_directory_for_each_user):
                for file in files:
                    filepath = subdir + os.sep + file
                    vd_kw = ['.mp4','.mkv','.m4v','.mov']
                    for vd in vd_kw:
                        if filepath.endswith(vd):
                            fl_lst.append(filepath)
            lst_txt = "လက်ရှိ ဖိုင်များ 👇\n" + "\n".join(['<code>{}</code>'.format(fl) for fl in fl_lst])
            fl_msg = await bot.send_message(
                text=lst_txt,
                chat_id=update.chat.id
            )
            for fl in fl_lst:
                if os.path.isfile(fl):
                    os.remove(fl)
            try:
                shutil.rmtree(outpath)
            except:
                pass
            await fl_msg.edit_text("ဖိုင်အားလုံးကို ဖျက်ပြီးပါပြီ ⚠️")
@pyrogram.Client.on_message(pyrogram.filters.command(["flrm"]))
async def remove_file(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        fl_path = update.reply_to_message.text
        if os.path.isfile(fl_path):
            os.remove(fl_path)
        await bot.send_message(
            text="အဆိုပါဖိုင်ကို ဖျက်ပြီးပါပြီ ⚠️",
            chat_id=update.chat.id
        )
    
