from requests import post,get
#from requests_html import HTMLSession
from config import Config
import pyrogram
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from trnl import Trnl

def transloader(base, last_url):
    req = requests.get(base)
    req.encoding = req.apparent_encoding
    html_text = req.text
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }
    data = dict(
        link=last_url,
        referer="",
        iuser="",
        ipass="",
        comment="",
        cookie="",
        method="tc",
        partSize=10,
        proxy="",
        proxyuser="",
        proxypass="",
        premium_user="",
        premium_pass=""
    )
    r = post(base + "/index.php", data=data, headers=headers, verify=False)
    # session = HTMLSession()
    # r = session.post(base+"/index.php",data=data,headers=headers,verify=False)
    soup = BeautifulSoup(r.text, "lxml")
    all_ = soup.find_all("input", type="hidden", attrs={"name": True}, value=True)
    data = {}
    for a in all_:
        data.update({a["name"]: a["value"]})
    j = post(base + "/index.php", data=data, headers=headers, verify=False)
    # j = session.post(base+"/index.php",data=data,headers=headers,verify=False)
    final = BeautifulSoup(j.text, "lxml")
    d = final.find_all("a", href=True)
    try:
        final_link = base + d[-2]["href"]
    except:
        final_link = "THE_ERROR"
    return final_link
