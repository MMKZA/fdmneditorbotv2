#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import asyncio
import json
import math
import os
import shutil
import multiprocessing
import time

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.display_progress import progress_for_pyrogram, humanbytes
from plugins.youtube_dl_button import youtube_dl_call_back
from plugins.dl_button import ddl_call_back
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from plugins.gdrv_id_save import cnmm_gdrv_id_save,gldchnl_gdrv_id_save,gdtot_gdrv_id_save
from plugins.methods import plhh_method,transload_method,direct_method
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image

@pyrogram.Client.on_callback_query()
def button(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        cb_data = update.data
        #logger.info(cb_data)
        if (":" in cb_data) and ('yoteshinportal.cc' not in cb_data) and ('gldchnl' not in cb_data) and ('gdtot' not in cb_data) and ('method=' not in cb_data):
            # unzip formats
            extract_dir_path = Config.DOWNLOAD_LOCATION + \
                "/" + str(update.from_user.id) + "zipped" + "/"
            if not os.path.isdir(extract_dir_path):
                bot.delete_messages(
                    chat_id=update.message.chat.id,
                    message_ids=update.message.message_id,
                    revoke=True
                )
                return False
            zip_file_contents = os.listdir(extract_dir_path)
            type_of_extract, index_extractor, undefined_tcartxe = cb_data.split(":")
            if index_extractor == "NONE":
                try:
                    shutil.rmtree(extract_dir_path)
                except:
                    pass
                bot.edit_message_text(
                    chat_id=update.message.chat.id,
                    text=Translation.CANCEL_STR,
                    message_id=update.message.message_id
                )
            elif index_extractor == "ALL":
                i = 0
                for file_content in zip_file_contents:
                    current_file_name = os.path.join(extract_dir_path, file_content)
                    start_time = time.time()
                    bot.send_document(
                        chat_id=update.message.chat.id,
                        document=current_file_name,
                        # thumb=thumb_image_path,
                        caption=file_content,
                        # reply_markup=reply_markup,
                        reply_to_message_id=update.message.message_id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                    i = i + 1
                    os.remove(current_file_name)
                try:
                    shutil.rmtree(extract_dir_path)
                except:
                    pass
                bot.edit_message_text(
                    chat_id=update.message.chat.id,
                    text=Translation.ZIP_UPLOADED_STR.format(i, "0"),
                    message_id=update.message.message_id
                )
            else:
                file_content = zip_file_contents[int(index_extractor)]
                current_file_name = os.path.join(extract_dir_path, file_content)
                start_time = time.time()
                bot.send_document(
                    chat_id=update.message.chat.id,
                    document=current_file_name,
                    # thumb=thumb_image_path,
                    caption=file_content,
                    # reply_markup=reply_markup,
                    reply_to_message_id=update.message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        start_time
                    )
                )
                try:
                    shutil.rmtree(extract_dir_path)
                except:
                    pass
                bot.edit_message_text(
                    chat_id=update.message.chat.id,
                    text=Translation.ZIP_UPLOADED_STR.format("1", "0"),
                    message_id=update.message.message_id
                )
        elif ("|" in cb_data) and ('yoteshinportal.cc' not in cb_data) and ('gldchnl' not in cb_data) and ('gdtot' not in cb_data) and ('method=' not in cb_data):
            youtube_dl_call_back(bot, update)
        elif ("=" in cb_data) and ('yoteshinportal.cc' not in cb_data) and ('gldchnl' not in cb_data) and ('gdtot' not in cb_data) and ('method=' not in cb_data):
            ddl_call_back(bot, update)
        if ('yoteshinportal.cc' in cb_data) and ('method=' not in cb_data):
            cnmm_gdrv_id_save(bot,update)
        if ('gldchnl' in cb_data) and ('method=' not in cb_data):
            gldchnl_gdrv_id_save(bot,update)
        if ('gdtot' in cb_data) and ('method=' not in cb_data):
            gdtot_gdrv_id_save(bot,update)
        if 'method=' in cb_data:
            if 'method=PLM' == cb_data:
                plhh_method(bot, update)
            elif 'method=TM' == cb_data:
                transload_method(bot, update)
            elif 'method=DM' == cb_data:
                direct_method(bot, update)
