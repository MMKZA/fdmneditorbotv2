import requests
from bs4 import BeautifulSoup

def mp4(url, base):
    #url = 'https://app.rapidleech.gq/files/Black.Site.2022.HD_GC.m4v'
    #base = 'https://app.rapidleech.gq/'
    base_host = base.split('/')[-1]
    kwd = url.split('/')[-1]
    nw_nm = kwd.replace('.m4v','.mp4')
    nw_url = 'https://app.rapidleech.gq/files/' + nw_nm
    r = requests.session()
    res = r.get(base)
    soup = BeautifulSoup(res.content, 'html.parser')
    sp1 = soup.find_all('tr',{'title':kwd})
    sp2 = "\n".join([str(lk) for lk in sp1[0].find_all('input')])
    fl_id = sp2.split('"')[-2]
    payload = {
        'act': 'rename_go',
        'files[]': fl_id,
        'newName[]': nw_nm
    }
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '76',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '_ga=GA1.2.1231193415.1658745553; showAll=1',
        'Host': base_host,
        'Origin': base,
        'Referer': base + 'index.php',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77'
    }
    res = r.post(base,headers=headers,data=payload)
    if '200' in res:
        return nw_url
    else:
        status = 'error'
        return status
