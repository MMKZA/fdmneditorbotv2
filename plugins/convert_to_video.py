#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import time
import shutil
from moviepy.editor import *
import random

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.display_progress import progress_for_pyrogram
from helper_funcs.ran_text import random_char
from helper_funcs.fdmn_frame import fdmn_frame
from helper_funcs.help_Nekmo_ffmpeg import generate_screen_shots

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from trnl import Trnl


@pyrogram.Client.on_message(pyrogram.filters.command(["convert2video"]))
async def convert_to_video(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return
    if update.reply_to_message is not None:
        vlink = Trnl.sh2.acell('C2').value
        nfh = random_char(5)
        download_location = Config.DOWNLOAD_LOCATION + "/" + f'{nfh}' + "/"
        dwnl_mssg = await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.DOWNLOAD_FILE,
            reply_to_message_id=update.message_id
        )
        c_time = time.time()
        the_real_download_location = await bot.download_media(
            message=update.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.DOWNLOAD_FILE,
                dwnl_mssg,
                c_time
            )
        )
        # don't care about the extension
        if the_real_download_location is not None:
            time.sleep(2)
            await dwnl_mssg.delete()
            up = await bot.send_message(
                chat_id=update.chat.id,
                text=Translation.UPLOAD_START
            )
            
            logger.info(the_real_download_location)
            ssimg = None
            try:
                is_w_f = False
                images = await generate_screen_shots(
                    the_real_download_location,
                    download_location,
                    is_w_f,
                    Config.DEF_WATER_MARK_FILE,
                    30,
                    9
                )
                ssimg = images[random.randint(0, 2)]
            except:
                pass
            if ssimg is None:
                width = 0
                height = 0
                clip = VideoFileClip(the_real_download_location)
                screen_time = random.randint(120,600)
                clip.save_frame(download_location + "thbnl1.jpg", t = screen_time)
                width = clip.w
                height = clip.h
                ssimg = download_location + "thbnl1.jpg"
            duration = 0
            metadata = extractMetadata(createParser(the_real_download_location))
            if metadata is not None:
                if metadata.has("duration"):
                    duration = metadata.get('duration').seconds
            try:
                metadata = extractMetadata(createParser(ssimg))
                width = metadata.get("width")
                height = metadata.get("height")
            except:
                img = Image.open(ssimg)
                width,height = img.size
            fdmn_frame(vlink,width,height)
            if 576 < width < 864:
                vd_qlt = '480p SD'
            elif 864 < width < 1296:
                vd_qlt = '720p HD'
            elif 1536 < width < 2304:
                vd_qlt = '1080p FHD'
            elif 3072 < width < 4608:
                vd_qlt = '4K'
            else:
                vd_qlt = 'HD'
            Trnl.sh2.update('H2',vd_qlt)
            #thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
            #if not os.path.exists(thumb_image_path):
                #thumb_image_path = None
            #else:
                #metadata = extractMetadata(createParser(thumb_image_path))
                #if metadata.has("width"):
                    #width = metadata.get("width")
                #if metadata.has("height"):
                    #height = metadata.get("height")
                # get the correct width, height, and duration for videos greater than 10MB
                # resize image
                # ref: https://t.me/PyrogramChat/44663
                # https://stackoverflow.com/a/21669827/4723940
                #Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
                #img = Image.open(thumb_image_path)
                # https://stackoverflow.com/a/37631799/4723940
                # img.thumbnail((90, 90))
                #img.resize((90, height))
                #img.save(thumb_image_path, "JPEG")
                # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
            # try to upload file
            c_time = time.time()
            if "@" in str(Trnl.sh2.acell('J2').value):
                chnl_id = update.message.chat.id
            else:
                chnl_id = int(Trnl.sh2.acell('J2').value)
            vd_name = the_real_download_location.split('/')[-1].replace('.mp4','') + ' | {} @fdmnchannel'.format(vd_qlt)
            ssimg = 'thumb_poster.jpg'
            vdf_msg = await bot.send_video(
                chat_id=chnl_id,
                video=the_real_download_location,
                caption=vd_name,
                duration=duration,
                width=width,
                height=height,
                supports_streaming=True,
                # reply_markup=reply_markup,
                thumb=ssimg,
                reply_to_message_id=update.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START,
                    up,
                    c_time
                )
            )
            Trnl.sh2.update('P2',str(vdf_msg.message_id))
            try:
                os.remove(the_real_download_location)
                os.remove(thumb_image_path)
                shutil.rmtree(download_location)
            except:
                pass
            await bot.edit_message_text(
                text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG,
                chat_id=update.chat.id,
                message_id=up.message_id,
                disable_web_page_preview=True
            )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.REPLY_TO_DOC_FOR_C2V,
            reply_to_message_id=update.message_id
        )
    
            
