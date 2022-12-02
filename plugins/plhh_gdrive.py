import requests
import json

def plhh_gdrive(gdrv_lk):
    gdrv_id = gdrv_lk.split('/')[5]
    plr_web = 'https://api.a-u.workers.dev/info/{}?_=1669997773466'.format(gdrv_id)
    req = requests.get(plr_web)
    response = json.loads(req.content)
    url = 'https://api.a-u.workers.dev/download/{}'.format(gdrv_id)
    if response['name'] is not None:
        return url#response['url']
#gdrv_lk = 'https://drive.google.com/file/d/1kAT4BdsylhdPcPK4neP40IxzKrHKZ83M/view?usp=share_link'   
#print(plhh_gdrive(gdrv_lk))
