import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests, zipfile, io
import os
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
import subprocess
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
class Trnl(object):
    with open('fdmn-channel-698f5c18ea12.txt','w',encoding = 'utf-8') as f:
        f.write('\n{')
        f.write('\n"type": "service_account",')
        f.write('\n"project_id": "fdmn-channel",')
        f.write('\n"private_key_id": "698f5c18ea12cc277c5e8dcbdca487a03729f843",')
        f.write('\n"private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCw4vvBxBqU2MiP\\nqgkVwbO0aig6IzzjDuwIIi8aqRj6e2CBmn77kBsOXrqgpD0o0PiFGLkHXlFK7TDs\\nz35zLkXD94I7hYotnIcDv1wsVVgpnifBJqNtTqdHkcM8vtpJ6OwhTFRvCG274i2D\\naAmg/laemimiMmPrEYdy/9zh8B/Z6K/9y81FwDXrM/MNZa5iGRD1PaUJs3ka6u1x\\ngLsAzkefvgFqVE0ZmOZ8E/1iy9Z314UktBkgkno7AE8r/OCLoec52lW95blA3WFw\\nDqXDXOsy9KHEYPtS7TNMWBW5FUmWFN+XjSEKoIRlv7QXVVcf0mbVwrsvVDe6Tg4q\\nTsO3WFPPAgMBAAECggEAA+r04zTnZV9AtYM4Y9kyBjMsnV0IqYl02cPvLHxwivgr\\nQwjw+p+jzxsBId26R7i1ncQrv6J501qS4taHdZITd7np56JB/+X095hIHCF9HfX5\\nBhuAiHwkmiIYXHuhO+ARRX1PwXB7r4BOg4mwl5LuHYxKzDhvuMfQ1YiP6TS+jhQX\\nxCFfIlH7H6IFF3ytRFTO/yonUwf53J1j/aJQXvliLrHyiepIUoqAXlGA5hzhq3Bv\\ncdraAyi6XrvFallIceNb2AXwqTLnr7trFoDS2HAiS8liaAZ74kbubwhQaLy1U1tN\\nTdZTsRGcfRuCp1DcWrrSACrYSYn/yb45Ftqhj2DeQQKBgQD1+YypGAPKQVRWzwAj\\nu/y7Q9BlTiu9eGE/k6KN4NDpIAGiK1a3YVXucL44hNSt4uT9gt2jNvCOQcJTjRr1\\nS+Pev/kE9Lc3Wa/c1wFZosW+YRPYbxFYlpZbH0Gq5pKLTIuzw1BodFe0XyeJoJWk\\nXRKk9EINsxgW+Gn7WK52KXtWwwKBgQC4GJUZztovzr9EWGvqGUgc3q+rxV+Fhkt+\\nJX7mgnF8bXMZ5qoal1AYMZHKvC6JF/JVsKOc/B40BkSehO6YOv7dPTXZUyJv4UzY\\nIRAJv89xQzLH1Jr6ZA2qciEE5TQ7OAYnjV2HeAinzlC478esU788kpQJXHpxnbcN\\nYJF+bKu2BQKBgA+dB5C0NYlhHDlmalvaUvCQHWpQy/X67jFa7baTzq79mRzyI08A\\nnrPD9E8iH13qSR7Ob8MseZiOFAe5rTxk1NIO3X+zCO46gy9BdpR6AJNVFi1m33MA\\nHAsssL5oZGTzNuryOuhmeiq434mc5+LHBafy2T6FX8IVgqSxvGFDwNCBAoGAcBHG\\n8qcR+/iIRzrstt4dIDYQCylkNQzD+E8rKXhPTcfzQdlBxF5Iy/GhJyHX0m1ZgQC/\\nGVoBqPoH29hgxxti+5u/pEUPubwV45x8/vJdfj3CNBQhJDy0dQZ1Q12kpkg8tudA\\nAK/51O2sBmkxzJ5O1LkGlYxOncu9G8+lwqi0/2ECgYAmIlDURloIf2zyQ/56QrGh\\nB9wLamlbM5T/CPqqcxAtoE1cWv2STSZpbdKHKw/KfIT/kzHsKoQEUza7ciI9lZhT\\nQxAobLogbj+gSXaWqwWB9eavnvT2dz2/MeJi9lyi+g+c9sePNep2qjXCSoxavM/J\\ndDu+UV5w204bphGvhz2r0w==\\n-----END PRIVATE KEY-----\\n",')
        f.write('\n"client_email": "fdmnchannel-mmkza5@fdmn-channel.iam.gserviceaccount.com",')
        f.write('\n"client_id": "106230405613252480679",')
        f.write('\n"auth_uri": "https://accounts.google.com/o/oauth2/auth",')
        f.write('\n"token_uri": "https://oauth2.googleapis.com/token",')
        f.write('\n"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",')
        f.write('\n"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/fdmnchannel-mmkza5%40fdmn-channel.iam.gserviceaccount.com"')
        f.write('\n}')
    my_json = 'fdmn-channel-698f5c18ea12.txt'
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(my_json, scope)
    gclient = gspread.authorize(creds)
    sh = gclient.open('tgtofbposts')
    sh1 = sh.worksheet("Sheet1")
    sh2 = sh.worksheet("Sheet2")
    sh3 = sh.worksheet("Sheet3")
    sh4 = sh.worksheet("Sheet4")
    #JSDL
    dl_js_dir = Config.DOWNLOAD_LOCATION + "/myjsons"
    if not os.path.isdir(dl_js_dir):
        zip_file_url = sh1.acell('U2').value
        r = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(dl_js_dir)
        del r
    #YTDLP
    dl_dir = Config.DOWNLOAD_LOCATION + "/ytdlp"
    if not os.path.isdir(dl_dir):
        zip_file_url = 'https://github.com/yt-dlp/yt-dlp/archive/refs/heads/master.zip'
        r = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(dl_dir)
        cd_dir  = Config.DOWNLOAD_LOCATION + "/ytdlp/yt-dlp-master/"
        with cd(cd_dir):
            process = subprocess.run(['python', 'setup.py', 'install'],shell=False)
        del r
        cmd0 = ['apt-get', 'install', 'wget']
        subprocess.run(cmd0,shell=False)
        cmd1 = ['wget', '-q', '-O', '- https://dl-ssl.google.com/linux/linux_signing_key.pub', '| apt-key add -']
        subprocess.run(cmd1,shell=False)
        cmd2 = ['sh', '-c', "'echo", '"deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main"', ">> /etc/apt/sources.list.d/google-chrome.list'"]
        subprocess.run(cmd2,shell=False)
        cmd3 = ['apt-get', '-y', 'update']
        subprocess.run(cmd3,shell=False)
        cmd4 = ['apt-get', 'install', '-y', 'google-chrome-stable']
        subprocess.run(cmd4,shell=False)
