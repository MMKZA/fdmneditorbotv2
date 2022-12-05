#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import asyncio
import json
import math
import os
import shutil
import time
import random
import io
import locale
from datetime import datetime
from pprint import pprint
import math
from moviepy.editor import *
from asgiref.sync import async_to_sync
from PIL import Image

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

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from pyrogram.types import InputMediaPhoto
from pyrogram.types.bots_and_keyboards import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from helper_funcs.display_progress import progress_for_pyrogram, humanbytes
from helper_funcs.get_duration import get_duration
#from helper_funcs.download_progress import download_progress
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from helper_funcs.help_Nekmo_ffmpeg import generate_screen_shots, repair_moov_atom
from helper_funcs.fdmn_frame import fdmn_frame
from trnl import Trnl
from plugins.scpt_auto import scpt_auto

from helper_funcs.file_extract import file_extract

from subprocess import PIPE, Popen

def youtube_dl_call_back(bot, update):
    if Trnl.sh2.acell('V2').value == 'auto':
        cb_data = Trnl.sh2.acell('V3').value
    elif Trnl.sh2.acell('V2').value == 'manual':
        cb_data = update.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("|")
    thumb_image_path = Config.DOWNLOAD_LOCATION + \
                       "/" + str(update.from_user.id) + ".jpg"
    save_ytdl_json_path = Config.DOWNLOAD_LOCATION + \
                          "/" + str(update.from_user.id) + ".json"
    try:
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
    except (FileNotFoundError) as e:
        bot.delete_messages(
            chat_id=act_chatid,
            message_ids=act_messageid,
            revoke=True
        )
        return False
    vcap = Trnl.sh2.acell('D2').value
    typ = Trnl.sh2.acell('P3').value
    vlink = Trnl.sh2.acell('C2').value
    youtube_dl_url = Trnl.sh2.acell('L2').value
    # youtube_dl_url = update.message.reply_to_message.text
    custom_file_name = str(response_json.get("title")) + \
                       "_" + youtube_dl_format + "." + youtube_dl_ext
    youtube_dl_username = None
    youtube_dl_password = None
    if "|" in youtube_dl_url:
        url_parts = youtube_dl_url.split("|")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
        elif len(url_parts) == 4:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in update.message.reply_to_message.entities:
                if entity.type == "text_link":
                    youtube_dl_url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    youtube_dl_url = youtube_dl_url[o:o + l]
        if youtube_dl_url is not None:
            youtube_dl_url = youtube_dl_url.strip()
        if custom_file_name is not None:
            custom_file_name = custom_file_name.strip()
        # https://stackoverflow.com/a/761825/4723940
        if youtube_dl_username is not None:
            youtube_dl_username = youtube_dl_username.strip()
        if youtube_dl_password is not None:
            youtube_dl_password = youtube_dl_password.strip()
        #logger.info(youtube_dl_url)
        #logger.info(custom_file_name)
    try:
        user = bot.get_me()
        mention = user["mention"]
        description = Translation.CUSTOM_CAPTION_UL_FILE.format(mention)
    except:
        pass
    if "fulltitle" in response_json:
        description = response_json["fulltitle"][0:1021]
        # escape Markdown and special characters
    try:
        b = bot.edit_message_text(
            text=Translation.DOWNLOAD_START,
            chat_id=update.message.chat.id,
            message_id=update.message.message_id
        )
    except:
        b = bot.send_message(
            chat_id=update.chat.id,
            text='Now Initializing...'
        )
    aud_ext = Trnl.sh2.acell('E3').value
    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    fl_fll_nm = Trnl.sh2.acell('D6').value
    if os.path.splitext(fl_fll_nm)[1] == '':
        fl_fll_nm = fl_fll_nm + '.mp4'
    if typ == 'Series':
        download_directory = tmp_directory_for_each_user + "/" + fl_fll_nm
        vcap = os.path.splitext(fl_fll_nm)[0]
    elif typ == 'Movie':
        download_directory = tmp_directory_for_each_user + "/" + fl_fll_nm
    #download_directory = tmp_directory_for_each_user + "/" + custom_file_name
    command_to_exec = []
    if tg_send_type == "audio":
        command_to_exec = [
            "yt-dlp",
            "-c",
            #"--max-filesize", str(4294967296),#"--max-filesize", str(Config.TG_MAX_FILE_SIZE),
            "--prefer-ffmpeg",
            "--extract-audio",
            "--audio-format", youtube_dl_ext,
            "--audio-quality", youtube_dl_format,
            youtube_dl_url,
            "-o", download_directory
        ]
    else:
        # command_to_exec = ["youtube-dl", "-f", youtube_dl_format, "--hls-prefer-ffmpeg", "--recode-video", "mp4", "-k", youtube_dl_url, "-o", download_directory]
        minus_f_format = youtube_dl_format
        if "youtu" in youtube_dl_url:
            minus_f_format = youtube_dl_format + "+bestaudio"
        command_to_exec = [
            "yt-dlp",
            "-c",
            #"--max-filesize", str(4294967296), #"--max-filesize", str(Config.TG_MAX_FILE_SIZE),
            "--embed-subs",
            "-f", minus_f_format,
            "--hls-prefer-ffmpeg", youtube_dl_url,
            "-o", download_directory
        ]
    if Config.HTTP_PROXY != "":
        command_to_exec.append("--proxy")
        command_to_exec.append(Config.HTTP_PROXY)
    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)
    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)
    command_to_exec.append("--no-warnings")
    # command_to_exec.append("--quiet")
    #logger.info(command_to_exec)
    start = datetime.now()
    process = Popen(
        *command_to_exec,
        stdout=PIPE,
        bufsize=1
    )
    # Wait for the subprocess to finish
    process.communicate("n\n")[0]
    #e_response = stderr.decode().strip()
    #t_response = stdout.decode().strip()
    ##logger.info(e_response)
    ##logger.info(t_response)
    #ad_string_to_replace = "please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output."
    #if e_response and ad_string_to_replace in e_response:
        #error_message = e_response.replace(ad_string_to_replace, "")
        #bot.edit_message_text(
            #chat_id=act_chatid,
            #message_id=act_messageid,
            #text=error_message
        #)
        #return False
    if os.path.exists(download_directory):
        # #logger.info(t_response)
        os.remove(save_ytdl_json_path)
        end = datetime.now()
        time_taken_for_download = (end - start).seconds
        file_size = Config.TG_MAX_FILE_SIZE + 1

        try:
            file_size = os.path.getsize(download_directory)
        except FileNotFoundError as exc:
            # download_directory = os.path.splitext(download_directory)[0]
            # custom_file_name = str(response_json.get("title")) + \
            # "." + youtube_dl_ext
            download_directory = os.path.splitext(download_directory)[0]# + "." + "mkv"
            # https://stackoverflow.com/a/678242/4723940
            file_size = os.path.getsize(download_directory)
        fl_ext = os.path.splitext(download_directory.split('/')[-1])[1]
        arc_kw = ['.zip','.rar','.7z']
        if fl_ext in arc_kw:
            Trnl.sh2.update('I3',download_directory)
            c = b.edit_text(
                text="ဖိုင်ကို Extract လုပ်နေပါတယ်...ဒါပြီးရင် Upload တင်မည့်ဖိုင်ကို /upload ဖြင့် Reply လုပ်ပါ 👇"
            )
            file_extract(bot,update)
        if fl_ext not in arc_kw:
            c = b.edit_text(
                text="Now Initializing..."
            )
            try:
                rntm = get_duration(download_directory)
                Trnl.sh2.update('M4',rntm)
            except:
                repaired_directory = async_to_sync(repair_moov_atom)(download_directory)
                if os.path.lexists(repaired_directory):
                    download_directory = repaired_directory
                    rntm = get_duration(download_directory)
                    Trnl.sh2.update('M4',rntm)
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
                chnl_id = update.from_user.id
            else:
                chnl_id = int(Trnl.sh2.acell('J2').value)
            if file_size > Config.TG_MAX_FILE_SIZE:
                d_f_s = humanbytes(os.path.getsize(download_directory))
                i_m_s_g = c.edit_text(
                    text="𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢 𝙎𝙪𝙥𝙥𝙤𝙧𝙩𝙨 2𝙂𝘽 𝙈𝙖𝙭\n𝘿𝙚𝙩𝙚𝙘𝙩𝙚𝙙 𝙁𝙞𝙡𝙚 𝙎𝙞𝙯𝙚: {} \n𝙩𝙧𝙮𝙞𝙣𝙜 𝙩𝙤 𝙨𝙥𝙡𝙞𝙩 𝙩𝙝𝙚 𝙛𝙞𝙡𝙚𝙨".format(d_f_s)
                )
                splitted_dir = async_to_sync(split_large_files)(download_directory)
                totlaa_sleif = os.listdir(splitted_dir)
                totlaa_sleif.sort()
                number_of_files = len(totlaa_sleif)
                #logger.info(totlaa_sleif)
                ba_se_file_name = os.path.basename(download_directory)
                i_m_s_g.edit_text(
                    f"𝘿𝙚𝙩𝙚𝙘𝙩𝙚𝙙 𝙁𝙞𝙡𝙚 𝙎𝙞𝙯𝙚: {d_f_s} \n"
                    f"<code>{ba_se_file_name}</code> 𝙨𝙥𝙡𝙞𝙩𝙩𝙚𝙙 𝙞𝙣𝙩𝙤 {number_of_files} 𝙛𝙞𝙡𝙚𝙨.\n"
                    "𝙩𝙧𝙮𝙞𝙣𝙜 𝙩𝙤 𝙪𝙥𝙡𝙤𝙖𝙙 𝙩𝙤 𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢, 𝙣𝙤𝙬 "
                )
                for le_file in totlaa_sleif:
                    i_th = totlaa_sleif.index(le_file) + 1
                    dwnl_dir = tmp_directory_for_each_user + "/fdmnsplits/" + le_file
                    upmssg = i_m_s_g.edit_text(
                        text=Translation.UPLOAD_START + f"\n<code>{ba_se_file_name} Part {i_th} of {number_of_files}</code>"
                    )
                    duration = 0
                    if tg_send_type != "file":
                        metadata = extractMetadata(createParser(dwnl_dir))
                        if metadata is not None:
                            if metadata.has("duration"):
                                duration = metadata.get('duration').seconds
                    if typ == 'Series':
                        vd_name = '{} | Part {} of {} @fdmnchannel'.format(vcap.replace('.',' ').replace('_',' '),i_th,number_of_files)
                    if typ == 'Movie':
                        vd_name = "{} | {} | Part {} of {} @fdmnchannel".format(vcap,vd_qlt,i_th,number_of_files)
                    ssimg = thumb_poster
                    start_time = time.time()
                    start_one = datetime.now()
                    vdf_msg = bot.send_video(
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
                            Translation.UPLOAD_START + f"\n<code>{ba_se_file_name} Part {i_th} of {number_of_files}</code>",
                            upmssg,
                            start_time
                        )
                    )
                    Trnl.sh2.update('P2',str(vdf_msg.message_id-i_th+1))
                end_one = datetime.now()
                time_taken_for_upload = (end_one - start_one).seconds
                if typ == 'Movie':
                    scpt_auto(bot, update)
                try:
                    shutil.rmtree(tmp_directory_for_each_user)
                    os.remove(thumb_image_path)
                except:
                    pass
                upmssg.edit_text(
                    text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download,time_taken_for_upload),
                    disable_web_page_preview=True
                )
            if file_size < Config.TG_MAX_FILE_SIZE:
                upmssg = c.edit_text(
                    text=Translation.UPLOAD_START + '\n<code>{}</code>'.format(vcap)
                )
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
                if tg_send_type == "audio":
                    bot.send_audio(
                        chat_id=act_chatid,
                        audio=download_directory,
                        caption=description,
                        parse_mode="HTML",
                        duration=duration,
                        # performer=response_json["uploader"],
                        # title=response_json["title"],
                        # reply_markup=reply_markup,
                        thumb=thumb_image_path,
                        reply_to_message_id=update.message.reply_to_message.message_id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            upmssg,
                            start_time
                        )
                    )
                elif tg_send_type == "file":
                    bot.send_document(
                        chat_id=act_chatid,
                        document=download_directory,
                        thumb=thumb_image_path,
                        caption=description,
                        parse_mode="HTML",
                        # reply_markup=reply_markup,
                        reply_to_message_id=update.message.reply_to_message.message_id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                elif tg_send_type == "vm":
                    bot.send_video_note(
                        chat_id=act_chatid,
                        video_note=download_directory,
                        duration=duration,
                        length=width,
                        thumb=thumb_image_path,
                        reply_to_message_id=update.message.reply_to_message.message_id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                elif tg_send_type == "video":
                    if typ == 'Series':
                        vd_name = '{} @fdmnchannel'.format(vcap.replace('.',' ').replace('_',' '))
                    if typ == 'Movie':
                        vd_name = "{} | {} @fdmnchannel".format(vcap,vd_qlt)
                    vdf_msg = bot.send_video(
                        # chat_id=act_chatid,
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
                            upmssg,
                            start_time
                        )
                    )
                    Trnl.sh2.update('P2',str(vdf_msg.message_id))
                    # vdf_msg = bot.forward_messages(
                    # chat_id=int("-1001785695486"),
                    # from_chat_id=act_chatid,
                    # message_ids=vd_msg.message_id
                    # )
                else:
                    logger.info("Did this happen? :\\")
                end_one = datetime.now()
                time_taken_for_upload = (end_one - start_one).seconds
                try:
                    shutil.rmtree(tmp_directory_for_each_user)
                    os.remove(thumb_image_path)
                except:
                    pass
                upmssg.edit_text(
                    text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download,time_taken_for_upload),
                    disable_web_page_preview=True
                )
                typ = Trnl.sh2.acell('P3').value
                Trnl.sh2.update('C3','close')
                Trnl.sh2.update('N7','close')
                if typ == 'Movie':
                    scpt_auto(bot, update)
