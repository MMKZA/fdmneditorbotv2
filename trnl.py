import gspread
from oauth2client.service_account import ServiceAccountCredentials
#
class Trnl(object):
    acc = 2
    if acc == 1:
        my_json = 'gsprd_aa.json'
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(my_json, scope)
        gclient = gspread.authorize(creds)
        sh = gclient.open('tgtofbposts')
        sh1 = sh.worksheet("Sheet1")
        sh2 = sh.worksheet("Sheet2")
        sh3 = sh.worksheet("Sheet3")
        sh4 = sh.worksheet("Sheet4")
    if acc == 2:
        my_json = 'gsprd_tp.json'
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(my_json, scope)
        gclient = gspread.authorize(creds)
        sh = gclient.open('tgtofbposts')
        sh1 = sh.worksheet("Sheet1")
        sh2 = sh.worksheet("Sheet2")
        sh3 = sh.worksheet("Sheet3")
        sh4 = sh.worksheet("Sheet4")
    if acc == 3:
        my_json = 'gsprd_rb.json'
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(my_json, scope)
        gclient = gspread.authorize(creds)
        sh = gclient.open('tgtofbposts')
        sh1 = sh.worksheet("Sheet1")
        sh2 = sh.worksheet("Sheet2")
        sh3 = sh.worksheet("Sheet3")
        sh4 = sh.worksheet("Sheet4")
    if acc == 4:
        my_json = 'gsprd_ait.json'
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(my_json, scope)
        gclient = gspread.authorize(creds)
        sh = gclient.open('tgtofbposts')
        sh1 = sh.worksheet("Sheet1")
        sh2 = sh.worksheet("Sheet2")
        sh3 = sh.worksheet("Sheet3")
        sh4 = sh.worksheet("Sheet4")
