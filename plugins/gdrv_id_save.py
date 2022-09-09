import pyrogram
from trnl import Trnl
import asyncio
from plugins.ytsn_dllk import ytsn_dllk
from plugins.gdrvclean import gdrvclean
from plugins.methods import methods
import os
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def cnmm_gdrv_id_save(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        index = int(update.data.split('|')[1])
        ytsn_lst_txt = Trnl.sh1.acell('A6').value
        ytsn_lst = ytsn_lst_txt.split('\n')
        logger.info(ytsn_lst)
        lk = ytsn_lst[index].split('|')[0].strip()
        logger.info(lk)
        gdrv_retrn = ytsn_dllk(lk)
        logger.info(gdrv_retrn)
        if "error" in gdrv_retrn:
            gdrvclean(gdrv_retrn)
            gdrv_lk = ytsn_dllk(lk)
        else:
            gdrv_lk = gdrv_retrn
        gdrv_id = gdrv_lk.split('/')[5]
        logger.info(gdrv_id)
        Trnl.sh1.update('L4',gdrv_id)
        methods(bot,update)
        
def gldchnl_gdrv_id_save(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        gdrv_id = update.data.split('|')[1]
        Trnl.sh1.update('L4',gdrv_id)
        methods(bot,update)
