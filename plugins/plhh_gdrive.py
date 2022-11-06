import requests
import json

def plhh_gdrive(gdrv_lk):
    gdrv_id = gdrv_lk.split('/')[5]
    plr_web = 'https://geolocation.zindex.eu.org/publiclinks.json?id={}'.format(gdrv_id)
    req = requests.get(plr_web)
    response = json.loads(req.content)
    return response['url']
