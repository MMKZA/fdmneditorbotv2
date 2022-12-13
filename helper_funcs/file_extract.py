import os
from trnl import Trnl
import pyrogram
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from multiprocessing import Process
import logging
import zipfile_deflate64 as zipfile
import rarfile
import py7zr
#import patoolib

def list_sorter(fl_lst):
    b = set(fl_lst)
    numList = sorted([x for x in b if x.split(' ')[0].isdigit()],
                 key=lambda x: int(x.split(' ')[0]))
    alphaList = sorted([x for x in b if not x.split(' ')[0].isdigit()])
    sortedList = numList + alphaList
    return sortedList

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

def zip_extract(inpath,outpath):
    with zipfile.ZipFile(inpath, 'r') as zip_file:
        zip_file.extractall(path=outpath)
        
def rar_extract(inpath,outpath):
    #patoolib.extract_archive(inpath, outdir=outpath)
    with rarfile.RarFile(inpath, 'r') as rar_file:
        rar_file.extractall(path=outpath)
        
def _7z_extract(inpath,outpath):
    #patoolib.extract_archive(inpath, outdir=outpath)
    with py7zr.SevenZipFile(inpath, mode='r') as _7z_file:
        _7z_file.extractall(path=outpath)

def list_sorter(fl_lst):
    b = set(fl_lst)
    numList = sorted([x for x in b if x.split(' ')[0].isdigit()],
                 key=lambda x: int(x.split(' ')[0]))
    alphaList = sorted([x for x in b if not x.split(' ')[0].isdigit()])
    sortedList = numList + alphaList
    return sortedList      
        
@pyrogram.Client.on_message(pyrogram.filters.command(["fldl"]))
def file_extract(bot,update):
    if update.from_user.id in Config.AUTH_USERS:
        inpath = Trnl.sh2.acell('I3').value
        fl_ext = os.path.splitext(inpath)[1]
        outpath = os.path.splitext(inpath)[0] + '/'
        if not os.path.isdir(outpath):
            os.makedirs(outpath)
        if fl_ext == '.zip':
            zip_extract(inpath,outpath)
        elif fl_ext == '.7z':
            _7z_extract(inpath,outpath)
        elif fl_ext == '.rar':
            rar_extract(inpath,outpath)
        fl_lst = []
        for subdir, dirs, files in os.walk(outpath):
            for file in files:
                filepath = subdir + os.sep + file
                filepath_ext = os.path.splitext(filepath)[1]
                vd_kw = ['.avi','.mkv','.m4v','.mov']
                if filepath_ext in vd_kw:
                    filepath_mp4 = os.path.splitext(filepath)[0] + '.mp4'
                    os.rename(filepath, filepath_mp4)
                    filepath = filepath_mp4
                fl_lst.append(filepath)
        try:
            if len(fl_lst) != 0:
                srtd_fl_lst = list_sorter(fl_lst)
                fl_lst_txt = 'ဖိုင်စာရင်း\n' + '\n'.join(srtd_fl_lst)
                for fl in srtd_fl_lst:
                    bot.send_message(
                        text='<code>{}</code>'.format(fl),
                        chat_id=update.message.chat.id,
                        parse_mode="html",
                    )
                bot.send_message(
                    text=fl_lst_txt,
                    chat_id=update.message.chat.id,
                    parse_mode="html",
                )
            if len(fl_lst) == 0:
                bot.send_message(
                        text='<code>{}</code>'.format("ဘာဖိုင်မှ မရှိပါ ⚠️"),
                        chat_id=update.message.chat.id,
                        parse_mode="html",
                )
        except:
            if len(fl_lst) != 0:
                srtd_fl_lst = list_sorter(fl_lst)
                fl_lst_txt = 'ဖိုင်စာရင်း\n' + '\n'.join(srtd_fl_lst)
                for fl in srtd_fl_lst:
                    bot.send_message(
                        text='<code>{}</code>'.format(fl),
                        chat_id=update.chat.id,
                        parse_mode="html",
                    )
                bot.send_message(
                    text=fl_lst_txt,
                    chat_id=update.chat.id,
                    parse_mode="html",
                )
            if len(fl_lst) == 0:
                bot.send_message(
                        text='<code>{}</code>'.format("ဘာဖိုင်မှ မရှိပါ ⚠️"),
                        chat_id=update.chat.id,
                        parse_mode="html",
                )
