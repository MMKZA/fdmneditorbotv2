import requests
import json

def plhh_gdrive(gdrv_lk):
    gdrv_id = gdrv_lk.split('/')[5]
    plr_web = 'https://api.a-u.workers.dev/info/{}?_=1669997773466'.format(gdrv_id)
    headers = {'accept-encoding' : 'utf-8'}
    req = requests.get(plr_web,headers=headers)
    response = json.loads(req.content.decode('utf-8'))
    url = 'https://api.a-u.workers.dev/download/{}'.format(gdrv_id)
    return url#response['url']
#gdrv_lk = 'https://drive.google.com/file/d/1kAT4BdsylhdPcPK4neP40IxzKrHKZ83M/view?usp=share_link'   
#print(plhh_gdrive(gdrv_lk))
