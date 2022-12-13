#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
import os
import shutil
import time
import random
from moviepy.editor import *

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
    
from helper_funcs.split_large_files import split_large_files

# the Strings used for this "thing"
from translation import Translation

import pyrogram
import re

logging.getLogger("pyrogram").setLevel(logging.WARNING)

from pyrogram import Client
from pyrogram.handlers import MessageHandler
from helper_funcs.display_progress import progress_for_pyrogram, humanbytes
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from helper_funcs.help_Nekmo_ffmpeg import generate_screen_shots, repair_moov_atom
from helper_funcs.fdmn_frame import fdmn_frame
from helper_funcs.get_duration import get_duration
from trnl import Trnl
from datetime import datetime
from asgiref.sync import async_to_sync

def extract_list_upload(bot, update, download_directory):
    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    typ = Trnl.sh2.acell('P3').value
    vlink = Trnl.sh2.acell('C2').value
    vd_name = os.path.splitext(download_directory.split('/')[-1])[0]
    upload_mssg = await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.UPLOAD_START + '\n<code>{}</code> @fdmnchannel'.format(vd_name),
        reply_to_message_id=update.message_id
    )
    tg_send_type = "video"
    try:
        vd_name = vd_name.replace('.',' ').replace('_',' ')
    except:
        pass
    try:
        rntm = get_duration(download_directory)
        Trnl.sh2.update('M4',rntm)
    except:
        repaired_directory = async_to_sync(repair_moov_atom)(download_directory)
        if os.path.lexists(repaired_directory):
            download_directory = repaired_directory
            rntm = get_duration(download_directory)
            Trnl.sh2.update('M4',rntm)
    try:
        file_size = os.path.getsize(download_directory)
    except FileNotFoundError as exc:
        download_directory = os.path.splitext(download_directory)[0]# + "." + "mkv"
        # https://stackoverflow.com/a/678242/4723940
        file_size = os.path.getsize(download_directory)
    ssimg = None
    width = 0
    height = 0
    try:
        is_w_f = False
        images = async_to_sync(generate_screen_shots)(
            download_directory,
            tmp_directory_for_each_user,
            is_w_f,
            Config.DEF_WATER_MARK_FILE,
            30,
            9
        )
        ssimg = images[random.randint(0, 2)]
    except:
        pass
    if ssimg is None:
        clip = VideoFileClip(download_directory)
        screen_time = random.randint(120,600)
        clip.save_frame(tmp_directory_for_each_user + "/thbnl1.jpg", t = screen_time)
        width = clip.w
        height = clip.h
        ssimg = tmp_directory_for_each_user + "/thbnl1.jpg"
    if width == 0 and height == 0:
        try:
            metadata = extractMetadata(createParser(ssimg))
            width = metadata.get("width")
            height = metadata.get("height")
        except:
            img = Image.open(ssimg)
            width,height = img.size
    Trnl.sh2.update('C5',width)
    Trnl.sh2.update('C6',height)
    thumb_poster = tmp_directory_for_each_user + '/' + os.path.splitext(vlink.split('/')[-1])[0] + '.jpeg'
    if not os.path.exists(thumb_poster):
        fdmn_frame(vlink,thumb_poster,width,height)
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
    if "@" in str(Trnl.sh2.acell('J2').value):
        chnl_id = update.message.chat.id
    else:
        chnl_id = int(Trnl.sh2.acell('J2').value)
        
    if file_size > Config.TG_MAX_FILE_SIZE:
        d_f_s = humanbytes(os.path.getsize(download_directory))
        i_m_s_g = await bot.edit_message_text(
            text="𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢 𝙎𝙪𝙥𝙥𝙤𝙧𝙩𝙨 2𝙂𝘽 𝙈𝙖𝙭\n𝘿𝙚𝙩𝙚𝙘𝙩𝙚𝙙 𝙁𝙞𝙡𝙚 𝙎𝙞𝙯𝙚: {} \n𝙩𝙧𝙮𝙞𝙣𝙜 𝙩𝙤 𝙨𝙥𝙡𝙞𝙩 𝙩𝙝𝙚 𝙛𝙞𝙡𝙚𝙨".format(d_f_s),
            chat_id=update.chat.id,
            message_id=upload_mssg.message_id
        )
        splitted_dir = await split_large_files(download_directory)
        totlaa_sleif = os.listdir(splitted_dir)
        totlaa_sleif.sort()
        number_of_files = len(totlaa_sleif)
        #logger.info(totlaa_sleif)
        ba_se_file_name = os.path.basename(download_directory)
        await i_m_s_g.edit_text(
            f"𝘿𝙚𝙩𝙚𝙘𝙩𝙚𝙙 𝙁𝙞𝙡𝙚 𝙎𝙞𝙯𝙚: {d_f_s} \n"
            f"<code>{ba_se_file_name}</code> 𝙨𝙥𝙡𝙞𝙩𝙩𝙚𝙙 𝙞𝙣𝙩𝙤 {number_of_files} 𝙛𝙞𝙡𝙚𝙨.\n"
            "𝙩𝙧𝙮𝙞𝙣𝙜 𝙩𝙤 𝙪𝙥𝙡𝙤𝙖𝙙 𝙩𝙤 𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢, 𝙣𝙤𝙬 "
        )
        for le_file in totlaa_sleif:
            i_th = totlaa_sleif.index(le_file) + 1
            dwnl_dir = tmp_directory_for_each_user + "/fdmnsplits/" + le_file
            upmssg = await bot.edit_message_text(
                text=Translation.UPLOAD_START + f"\n<code>{ba_se_file_name} Part {i_th}</code>",
                chat_id=update.chat.id,
                message_id=update.message_id
            )
            duration = 0
            if tg_send_type != "file":
                metadata = extractMetadata(createParser(dwnl_dir))
                if metadata is not None:
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
            if typ == 'Movie':
                vcap = Trnl.sh2.acell('D2').value
                vd_name = '{} | {} | Part {} @fdmnchannel'.format(vcap, vd_qlt, i_th)
            else:
                vd_name =  "<code>{} | Part {}</code> @fdmnchannel".format(vd_name,i_th)
            start_time = time.time()
            start_one = datetime.now()
            vdf_msg = await bot.send_video(
                # chat_id=update.message.chat.id,
                chat_id=chnl_id,
                video=dwnl_dir,
                caption=vd_name,
                parse_mode="HTML",
                duration=duration,
                width=width,
                height=height,
                supports_streaming=True,
                # reply_markup=reply_markup,
                thumb=thumb_poster,
                # reply_to_message_id=update.message.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START + f"\n<code>{ba_se_file_name} Part {i_th}</code>",
                    upmssg,
                    start_time
                )
            )
            Trnl.sh2.update('P2',str(vdf_msg.message_id-i_th+1))
        end_one = datetime.now()
        time_taken_for_upload = (end_one - start_one).seconds
        await bot.edit_message_text(
            text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download,
                                                                        time_taken_for_upload),
            chat_id=update.chat.id,
            message_id=upmssg.message_id,
            disable_web_page_preview=True
        )
        Trnl.sh2.update('C3','close')
        Trnl.sh2.update('N7','close')
    if file_size < Config.TG_MAX_FILE_SIZE:
        duration = 0
        if tg_send_type != "file":
            metadata = extractMetadata(createParser(download_directory))
            if metadata is not None:
                if metadata.has("duration"):
                    duration = metadata.get('duration').seconds
        # get the correct width, height, and duration for videos greater than 10MB
        if os.path.exists(thumb_image_path):
            width = 0
            height = 0
            metadata = extractMetadata(createParser(thumb_image_path))
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
            if tg_send_type == "vm":
                height = width
            # resize image
            # ref: https://t.me/PyrogramChat/44663
            # https://stackoverflow.com/a/21669827/4723940
            Image.open(thumb_image_path).convert(
                "RGB").save(thumb_image_path)
            img = Image.open(thumb_image_path)
            # https://stackoverflow.com/a/37631799/4723940
            # img.thumbnail((90, 90))
            if tg_send_type == "file":
                img.resize((320, height))
            else:
                img.resize((90, height))
            img.save(thumb_image_path, "JPEG")
            # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
        else:
            thumb_image_path = None
        start_time = time.time()
        start_one = datetime.now()
        # try to upload file                                              
        if tg_send_type == "video":
            if typ == 'Movie':
                vcap = Trnl.sh2.acell('D2').value
                vd_name = '{} | {} @fdmnchannel'.format(vcap, vd_qlt)
            else:
                vd_name = '<code>{}</code> @fdmnchannel'.format(vd_name)
            vdf_msg = await bot.send_video(
                # chat_id=update.message.chat.id,
                chat_id=chnl_id,
                video=download_directory,
                caption=vd_name,
                parse_mode="HTML",
                duration=duration,
                width=width,
                height=height,
                supports_streaming=True,
                # reply_markup=reply_markup,
                thumb=thumb_poster,
                # reply_to_message_id=update.message.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START + f"\n<code>{vd_name}</code>",
                    upload_mssg,
                    start_time
                )
            )
            Trnl.sh2.update('P2',str(vdf_msg.message_id))
            # vdf_msg = await bot.forward_messages(
            # chat_id=int("-1001785695486"),
            # from_chat_id=update.message.chat.id,
            # message_ids=vd_msg.message_id
            # )
        else:
            logger.info("Did this happen? :\\")
        end_one = datetime.now()
        time_taken_for_upload = (end_one - start_one).seconds
        await bot.edit_message_text(
            text='Upload ကြာချိန် : {} စက္ကန့်'.format(time_taken_for_upload),
            chat_id=update.chat.id,
            message_id=upload_mssg.message_id,
            disable_web_page_preview=True
        )
        Trnl.sh2.update('C3','close')
        Trnl.sh2.update('N7','close')
