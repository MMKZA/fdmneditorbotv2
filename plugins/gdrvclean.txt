from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from trnl import Trnl
import json

def gdrvclean(status):
    if "tharphyo" in Trnl.sh1.acell('N2').value:
        my_json = 'token.json'
    if "st121" in Trnl.sh1.acell('N2').value:
        my_json = 'aittoken.json'
    if "robert" in Trnl.sh1.acell('N2').value:
        my_json = 'roberttoken.json'
    if "error" in status:
        scope = ['https://www.googleapis.com/auth/drive']
        creds = Credentials.from_authorized_user_file(my_json, scope)
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
            
