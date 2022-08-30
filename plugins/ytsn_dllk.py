import requests
import json
from trnl import Trnl
from bs4 import BeautifulSoup
import re
from trnl import Trnl

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger('chardet.universaldetector').setLevel(logging.INFO)

def ytsn_lgn(eml, pswd, csrf):
    url_login = 'https://yoteshinportal.cc/login'
    r = requests.session()
    cookies = {
        '_ga' : 'GA1.2.197300883.1644724921',
        '__gads' : 'ID=482619c4e658619e:T=1658430248:S=ALNI_Ma1T3_FDX4ArBdB-_zkuvRhAv0ujQ',
        '__gpi' : 'UID=000007486aa5348d:T=1658430248:RT=1658430248:S=ALNI_MZ9O12EWFCVUPDiv11cumNXPj2Gag',
        '_gid' : 'GA1.2.1529347631.1661177160; adonis-session=5f5318372cf70368aeac07c6d4d3d52cFEbUbggJeKOEnXoIppjyhsODNKDgMCDd67CvLvYIv7QcWYqa%2BTNNNAo1x%2F%2FKtOwYbVOGl3WX36YP8ogmkRWdTDpADdMwG3wG7lVz96cgu16k9lVNDCt7AXSl8C2xESRr; XSRF-TOKEN=96d655338a4a47266cee637fda1c3340v9CqLA%2FFgFPDndtC9IsVw%2FaSr65jygGpDoyyJFxabKNl8PAKu%2BAgwd4aHfReQo%2FN5%2BeACFkz8GehZI5nUz388WNdNk2J7MMOpVgQy2fyb7WP4eT1IuPftjLwsh4FV0TS; adonis-session-values=4cb4ee797508ae1c1e1c68974c25c575iTjCAW9f1Xt2O0lphysWhnFcV4x%2FkMjEd%2FQrmfy2VSq4dbiz2wPvcnItPboK8Y%2F4d1KR2ivABl2zLM0MLkfNFVUNZ%2BF7J%2FXFV4nolNOtxq1w4o%2FQn1KX%2Fg8Q%2Fvtnv3LVRp88NqT%2Bxwg7pgFd0cj5%2BIFsQ1ltnANridBWSufnq2Y%3D'
        }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'content-length': '117',
        #'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',        
        'origin': 'https://yoteshinportal.cc',
        'referer': 'https://yoteshinportal.cc/login',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'Connection':'close',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62'
        }
    payload = {
        '_csrf': csrf, #'YQsY5w6s-AJAj2iMCdt_MXdcasxJs6tAHMF4',
        'username': eml,
        'password': pswd,
        'remember': 'true'
        }
    res = r.post(url_login,headers=headers,data=payload,cookies=cookies,allow_redirects=False)
    logger.info(res)
    html_text = res.text
    Trnl.sh2.update('A6',html_text)
    return [r,cookies]

def ytsn_dllk(ytsn_lk):
    acc_id = Trnl.sh2.acell('N2').value
    if "robert" in acc_id:
        eml = 'robertfalconscott1997@gmail.com'
        csrf = 'a68CI1uX-ZsR_78AIvDKeTwitEjh2P2JFSb4'
    if "tharphyo" in acc_id:
        eml = 'gantgawnitharphyoaung@gmail.com'
        csrf = 'sgWVjryl-b2oTJB6NAmpUUg0qSs0or87TTmU'
    if "st121" in acc_id:
        eml = 'st121485@ait.asia'
        csrf = 'fyYGZ6UJ-7JYRuoc8_CgHt3GOi4Uwi6hMp5k'
    pswd = 'Vending5'
    rtrn = ytsn_lgn(eml,pswd,csrf)
    session = rtrn[0]
    sv_url = 'https://yoteshinportal.cc/api/save'
    get_ytsn_lk = 'https://yoteshinportal.cc/drive/' + ytsn_lk.split('/')[-1]
    cookies = rtrn[1]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'referer': 'https://yoteshinportal.cc/login',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'Connection':'close',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62'
        }
    get = session.get(get_ytsn_lk,headers=headers,cookies=cookies,allow_redirects=False)
    logger.info(get)
    get_text = get.text
    Trnl.sh2.update('A5',get_text)
    soup = BeautifulSoup(get.content,'lxml')
    id_loc = soup.find_all('a', {'class':"butt text-decoration-none disabled"})
    for x in id_loc:
        if re.match('app.saveToGoogleDrive',x['onclick']):
            id_flt = x['onclick']
            vd_id = id_flt.split("'")[1]
    logger.info(vd_id)
    headers1 = {
        'accept': '*/*',
        'accept-encoding': 'utf-8',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '19',
        'content-type': 'application/json',
        'origin': 'https://yoteshinportal.cc',
        'referer': str(get_ytsn_lk),
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62',
        'x-requested-with': 'XMLHttpRequest'
    }
    payload1 = {"key":vd_id}
    req = session.post(sv_url,headers=headers1,json=payload1)
    info = req.content
    status = json.loads(info)['status']
    logger.info(status)
    if "success" in status:
        fileid = json.loads(info)['fileId']
        gdrv_lk = "https://drive.google.com/file/d/" + fileid + "/view?usp=sharing"
        logger.info(gdrv_lk)
        return gdrv_lk
    if "error" in status:
        return status
