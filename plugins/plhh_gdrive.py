import requests
import json
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def plhh_gdrive(gdrv_lk):
    logger.info(gdrv_lk)
    gdrv_id = gdrv_lk.split('/')[5]
    logger.info(gdrv_id)
    plr_web = 'https://api.a-u.workers.dev/info/{}?_=1669997773466'.format(gdrv_id)
    logger.info(plr_web)
    headers = {
      'accept': '*/*',
      'accept-encoding' : 'utf-8',
      'accept-language' : 'en-US,en;q=0.9',
      'origin': 'https://publiclinks.hashhackers.com',
      'referer': 'https://publiclinks.hashhackers.com/',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62'
    }
    req = requests.get(plr_web,headers=headers)
    logger.info(req)
    logger.info(req.content.decode('utf-8'))
    response = json.loads(req.content.decode('utf-8'))
    url = 'https://api.a-u.workers.dev/download/{}'.format(gdrv_id)
    return url#response['url']
#gdrv_lk = 'https://drive.google.com/file/d/1kAT4BdsylhdPcPK4neP40IxzKrHKZ83M/view?usp=share_link'   
#print(plhh_gdrive(gdrv_lk))
