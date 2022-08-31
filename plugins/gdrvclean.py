from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from trnl import Trnl
import json
import requests

def gdrvauth():
    if "tharphyo" in Trnl.sh2.acell('N2').value:
        client_id = '361597500565-vb5t244ml0no4hurcsnsi2ev2465r5lo.apps.googleusercontent.com'
        client_secret = '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'
        refresh_token = '1//0g2YEbK1fywuVCgYIARAAGBASNwF-L9IrM850SylhyzdhHQeWDgYNWmAfYTtTqQYqq8E3alIb3L-DhkVWBORZR1eXcls9YKTD8-4'
    if "st121" in Trnl.sh2.acell('N2').value:
        client_id = '98300816133-rkcep9nmlfghfcvuokejk8mdkgh8ie29.apps.googleusercontent.com'
        client_secret = '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'
        refresh_token = '1//0gbP5IYZ1-9dhCgYIARAAGBASNwF-L9Irj-9p1ncmil8BVpfyLrYtqbzG7rWZ2Z2EGMqsNbt_gqZW3lWdcRphxqcCkqvVm3oscBU'
    if "robert" in Trnl.sh2.acell('N2').value:
        client_id = '418134424748-p19effruii2fs8p0b1ldakalppkvbi0n.apps.googleusercontent.com'
        client_secret = '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'
        refresh_token = '1//0gnH7e9YpevauCgYIARAAGBASNwF-L9IrQuGVaJw9T1_i2DckjYkoABBJ1YfFfSGMJRDeGVd21xDbzJ8cbsLT781_HJRooAi8HDs'
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
    return service
def gdrvclean(status):
    if "error" in status:
        service = gdrvauth()
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
            
def poster_gdrvclean():
    service = gdrvauth()
    page_token = None
    results = service.files().list(q="name contains 'post_poster_v2'",
                                    spaces='drive',
                                    fields='nextPageToken, '
                                        'files(id, name)',
                                    pageToken=page_token).execute()
    ytsn_info = results.get('files', [])
    for a in ytsn_info:
        ytsn_id = u'{0}'.format(a['id'])
        service.files().delete(fileId=ytsn_id).execute()
