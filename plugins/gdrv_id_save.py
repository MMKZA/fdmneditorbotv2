import pyrogram
from trnl import Trnl
import asyncio
from plugins.ytsn_dllk import ytsn_dllk
from plugins.gdrvclean import gdrvclean
from plugins.methods import methods
from plugins.methods import plhh_method,transload_method,direct_method
from plugins.gdtot_dl import gdtot_dl
import os
import requests
import re

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
    
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def cnmm_gdrv_id_save(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        index = int(update.data.split('|')[1])
        ytsn_lst_txt = Trnl.sh2.acell('A6').value
        ytsn_lst = ytsn_lst_txt.split('\n')
        #logger.info(ytsn_lst)
        lk = ytsn_lst[index].split('|')[0].strip()
        #logger.info(lk)
        gdrv_retrn = ytsn_dllk(lk)
        #logger.info(gdrv_retrn)
        if "error" in gdrv_retrn:
            gdrvclean(gdrv_retrn)
            gdrv_lk = ytsn_dllk(lk)
        else:
            gdrv_lk = gdrv_retrn
        gdrv_id = gdrv_lk.split('/')[5]
        #logger.info(gdrv_id)
        Trnl.sh2.update('L4',gdrv_id)
        if Trnl.sh2.acell('W2').value == 'manual':
            methods(bot,update)
        elif Trnl.sh2.acell('W2').value == 'auto':
            if 'method=PLM' in Trnl.sh2.acell('W3').value:
                plhh_method(bot, update)
            elif 'method=TM' in Trnl.sh2.acell('W3').value:
                transload_method(bot, update)
            elif 'method=DM' in Trnl.sh2.acell('W3').value:
                direct_method(bot, update)
def gldchnl_gdrv_id_save(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        gdrv_id = update.data.split('|')[1]
        Trnl.sh2.update('L4',gdrv_id)
        methods(bot,update)
        if Trnl.sh2.acell('W2').value == 'manual':
            methods(bot,update)
        elif Trnl.sh2.acell('W2').value == 'auto':
            if 'method=PLM' in Trnl.sh2.acell('W3').value:
                plhh_method(bot, update)
            elif 'method=TM' in Trnl.sh2.acell('W3').value:
                transload_method(bot, update)
            elif 'method=DM' in Trnl.sh2.acell('W3').value:
                direct_method(bot, update)
def gdtot_gdrv_id_save(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        index = int(update.data.split('|')[1])
        url_lst_txt = Trnl.sh2.acell('A6').value
        url_lst = url_lst_txt.split('\n')
        url = url_lst[index].split('|')[0]
        res = requests.get(url)
        gdtot_lk = re.findall('https://[a-zA-Z]+\.gdtot\.[a-zA-Z]+/file/[0-9]+',res.text)[0] 
        gdtot_info = gdtot_dl(gdtot_lk)
        gdrv_lk = gdtot_info['gdrive_link']
        gdrv_id = gdrv_lk.split('/')[3].split('=')[1]
        Trnl.sh2.update('L4',gdrv_id)
        methods(bot,update)
        if Trnl.sh2.acell('W2').value == 'manual':
            methods(bot,update)
        elif Trnl.sh2.acell('W2').value == 'auto':
            if 'method=PLM' in Trnl.sh2.acell('W3').value:
                plhh_method(bot, update)
            elif 'method=TM' in Trnl.sh2.acell('W3').value:
                transload_method(bot, update)
            elif 'method=DM' in Trnl.sh2.acell('W3').value:
                direct_method(bot, update)
