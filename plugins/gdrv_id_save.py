import pyrogram
from trnl import Trnl
import asyncio
from plugins.ytsn_dllk import ytsn_dllk
from plugins.gdrvclean import gdrvclean, gdtotclean
from plugins.methods import methods
from plugins.methods import plhh_method,transload_method,direct_method
from plugins.gdtot_dl import gdtot_dl
import os
import requests
import re
from bs4 import BeautifulSoup

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
        gdrv = update.data
        gdrv_req = requests.get(gdrv)
        gdrv_req.encoding = gdrv_req.apparent_encoding
        gdrv_html = gdrv_req.text
        soup = BeautifulSoup(gdrv_html, 'html.parser')
        href_lst = []
        for a in soup.find_all('a', href=True):
            href_lst.append(a['href'])
        for h in href_lst:
            if 'followup=' in h:
                dllk = h.split('followup=')[1]
                gdrv_lst.append('{} | {} | {}'.format(dllk,al.split("|", 3)[1].strip(),al.split("|", 3)[2].strip()))
            elif ('followup=' not in h) and ('https://drive.google.com/file/d/' in h):
                dllk = h
        gdrv_id = dllk.split('/')[5]
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
def gdtot_gdrv_id_save(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        index = int(update.data.split('|')[1])
        url_lst_txt = Trnl.sh2.acell('A6').value
        url_lst = url_lst_txt.split('\n')
        url = url_lst[index].split('|')[0].strip()
        res = requests.get(url)
        #gdtot_lk = re.findall('https://[a-zA-Z]+\.gdtot\.[a-zA-Z]+/file/[0-9]+',res.text)[0]
        gdtot_lk = re.search("(?P<url>https?://[^\s]+)", re.findall('<a href="https://[A-Za-z0-9]+\.gdtot\.cfd/file/[0-9]+" class=', res.text)[0]).group("url").replace('"','')
        gdtot_info = gdtot_dl(gdtot_lk)
        if gdtot_info['error'] == True:
            try:
                status = 'error'
                gdtotclean(status)
                gdtot_info = gdtot_dl(gdtot_lk)
            except:
                pass
        gdrv_lk = gdtot_info['gdrive_link']
        gdrv_id = gdrv_lk.split('/')[3].split('=')[1]
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
