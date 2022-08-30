from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from trnl import Trnl
import json
import requests
import os
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
    
def gdrvclean(status):
    if "tharphyo" in Trnl.sh1.acell('N2').value:
        gsprd_json_path = Config.DOWNLOAD_LOCATION + "/myjsons/drvtokens/gsprd_tp.json"
        with open(gsprd_json_path, "r", encoding="utf8") as f:
            gsprd_json = json.load(f)
        client_id = gsprd_json['client_id']
        client_secret = gsprd_json['client_secret']
        refresh_token = gsprd_json['refresh_token']
    if "st121" in Trnl.sh1.acell('N2').value:
        gsprd_json_path = Config.DOWNLOAD_LOCATION + "/myjsons/drvtokens/tphatoken.json"
        with open(gsprd_json_path, "r", encoding="utf8") as f:
            gsprd_json = json.load(f)
        client_id = gsprd_json['client_id']
        client_secret = gsprd_json['client_secret']
        refresh_token = gsprd_json['refresh_token']
    if "robert" in Trnl.sh1.acell('N2').value:
        gsprd_json_path = Config.DOWNLOAD_LOCATION + "/myjsons/drvtokens/roberttoken.json"
        with open(gsprd_json_path, "r", encoding="utf8") as f:
            gsprd_json = json.load(f)
        client_id = gsprd_json['client_id']
        client_secret = gsprd_json['client_secret']
        refresh_token = gsprd_json['refresh_token']
    if "error" in status:
        scope = ['https://www.googleapis.com/auth/drive']
        params = {
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token
        }
        authorization_url = "https://oauth2.googleapis.com/token"
        r = requests.post(authorization_url, data=params)
        access_token = r.json()['access_token']
        creds = Credentials(access_token, scope)
        service = build('drive', 'v3', credentials=creds)
        page_token = None
        results = service.files().list(q="name contains 'YoteShin'",
                                        spaces='drive',
                                        fields='nextPageToken, '
                                               'files(id, name)',
                                        pageToken=page_token).execute()
        ytsn_info = results.get('files', [])
        for a in ytsn_info:
            ytsn_id = u'{0}'.format(a['id'])
        service.files().delete(fileId=ytsn_id).execute()
            
