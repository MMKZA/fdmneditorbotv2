import requests
from bs4 import BeautifulSoup
import urllib

def mp4(url, base):
    base_host = base.split('/')[-2]
    print(base_host)
    kwd = urllib.parse.unquote_plus(url.split('/')[-1])
    print(kwd)
    ext_lst = ['.m4v','.mkv']
    for e in ext_lst:
        if e in kwd:
            nw_nm = kwd.replace(e,'.mp4')
    nw_url = base + 'files/' + nw_nm    
    r = requests.session()
    res = r.get(base + 'index.php',cookies={"_ga":"GA1.2.1231193415.1658745553"})
    soup = BeautifulSoup(res.content, 'html.parser')
    sp1 = soup.find_all('tr',{'title':kwd})
    sp2 = "".join([str(lk) for lk in sp1[0].find_all('input')])
    fl_id = sp2.split('"')[-2]
    print(fl_id)
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
        'Content-Length': '124',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '_ga=GA1.2.1231193415.1658745553',
        'Host': base_host,
        'Origin': base.replace('/',''),
        'Referer': base + 'index.php',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63'
    }
    res = r.post(base,headers=headers,data=payload)
    print(res)
    nw_url = base + 'files/' + urllib.parse.quote_plus(nw_nm)
    return nw_url
