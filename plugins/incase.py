from requests import post,get
#from requests_html import HTMLSession
from config import Config
import pyrogram
import requests
from bs4 import BeautifulSoup as bs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from trnl import Trnl
from plugins.transloader import transloader
@pyrogram.Client.on_message(pyrogram.filters.command(["tran"]))
def incase(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        lk = update.text.split(" ", 1)
        base = Trnl.sh1.acell('K2').value
        final_link = transloader(base, lk)
        Trnl.sh2.update('L2',final_link)
        bot.send_message(
            chat_id=update.chat.id,
            text="Link မှန်ကန်ပါက ဇာတ်ကားတင်လို့ရပါပြီ 👇\n" + final_link
        )
