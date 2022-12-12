import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests, zipfile, io
import os
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
    
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger('chardet.universaldetector').setLevel(logging.INFO)
logging.getLogger("requests_cache").setLevel(logging.WARNING)
logging.getLogger("oauth2client").setLevel(logging.WARNING)

class Trnl(object):
    dl_js_dir = Config.DOWNLOAD_LOCATION + "/myjsons"
    if not os.path.isdir(dl_js_dir):
        zip_file_url = 'https://drive.google.com/uc?export=download&id=1OMsgEL-Bgj_ZmNf6sJC7a1wXOwM5W-bG'
        r = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(dl_js_dir)
        del r
    if os.path.isdir(dl_js_dir):
        acc = 1
        if acc == 1:
            my_json = Config.DOWNLOAD_LOCATION + '/myjsons/drvtokens/gsprd_aa.json'
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(my_json, scope)
            gclient = gspread.authorize(creds)
            sh = gclient.open('tgtofbposts')
            sh1 = sh.worksheet("Sheet1")
            sh2 = sh.worksheet("Sheet2")
            sh3 = sh.worksheet("Sheet3")
            sh4 = sh.worksheet("Sheet4")
            sh5 = sh.worksheet("Paid Members")
        if acc == 2:
            my_json = Config.DOWNLOAD_LOCATION + '/myjsons/drvtokens/gsprd_tp.json'
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(my_json, scope)
            gclient = gspread.authorize(creds)
            sh = gclient.open('tgtofbposts')
            sh1 = sh.worksheet("Sheet1")
            sh2 = sh.worksheet("Sheet2")
            sh3 = sh.worksheet("Sheet3")
            sh4 = sh.worksheet("Sheet4")
            sh5 = sh.worksheet("Paid Members")
        if acc == 3:
            my_json = Config.DOWNLOAD_LOCATION + '/myjsons/drvtokens/gsprd_rb.json'
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(my_json, scope)
            gclient = gspread.authorize(creds)
            sh = gclient.open('tgtofbposts')
            sh1 = sh.worksheet("Sheet1")
            sh2 = sh.worksheet("Sheet2")
            sh3 = sh.worksheet("Sheet3")
            sh4 = sh.worksheet("Sheet4")
            sh5 = sh.worksheet("Paid Members")
        if acc == 4:
            my_json = Config.DOWNLOAD_LOCATION + '/myjsons/drvtokens/gsprd_ait.json'
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(my_json, scope)
            gclient = gspread.authorize(creds)
            sh = gclient.open('tgtofbposts')
            sh1 = sh.worksheet("Sheet1")
            sh2 = sh.worksheet("Sheet2")
            sh3 = sh.worksheet("Sheet3")
            sh4 = sh.worksheet("Sheet4")
            sh5 = sh.worksheet("Paid Members")


