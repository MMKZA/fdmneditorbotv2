import requests
import json
from trnl import Trnl
from plugins.ytsn_lgn import ytsn_lgn

async def ytsn_dllk(ytsn_lk):
    acc_id = Trnl.sh1.acell('N2').value
    if "robert" in acc_id:
        eml = 'robertfalconscott1997@gmail.com'
    if "tharphyo" in acc_id:
        eml = 'gantgawnitharphyoaung@gmail.com'
    if "st121" in acc_id:
        eml = 'st121485@ait.asia'
    pswd = 'Vending5'
    session = await ytsn_lgn(eml,pswd)
    sv_url = 'https://yoteshinportal.cc/api/save'
    headers1 = {
        'accept': '*/*',
        'accept-encoding': 'utf-8',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '19',
        'content-type': 'application/json',
        'cookie': '_ga=GA1.2.197300883.1644724921; __gads=ID=482619c4e658619e:T=1658430248:S=ALNI_Ma1T3_FDX4ArBdB-_zkuvRhAv0ujQ; __gpi=UID=000007486aa5348d:T=1658430248:RT=1658430248:S=ALNI_MZ9O12EWFCVUPDiv11cumNXPj2Gag; _gid=GA1.2.2133751929.1658542817; adonis-remember-token=11f9f5a7a6f848e055cf3b3999443d567ZLJ%2FQKyK2197GINKM%2FykSKU6jzZkKad585RbZn5L2GtoBuyuq3p1YO6A797gj2i%2FOVjvUGYueuhYz0MlqFzLIsb%2B0vhfEuySSuUrzXWzSX%2FtZQGDqkUGG%2BJmNjxWZJd; adonis-session=feabd6a5c3394bac6deeadd41697e0c0kDOrFndcgUv9zANt202KJRO5m%2FsRSJekwd7akDcCV%2FAqOARAIZt2RZ2GjhR8x1FBBTIs8lGmJEjKIRFma6tEverVEpDTotdllc7eSFSzT%2FtnVylBykcDBlUlg0UtGsu5; XSRF-TOKEN=833767e942db2789e9344991a09d2636UbwlW3aAb1fx1DbLat0OkSgYhEKUPx16lMzjqweqBbxFY4ZVaf7u3TznTlLLGKkaOXt0MFMxx0Nw5uq2b6PlwAzfv75HlgA1wuXa0mXGTkw4VHcsydKFAdd9ZqDmZu3y; adonis-session-values=659391fd9b5157a0b74a7b944a999a75GkuoP3rPQzfPsD3gx2psTdBlGp51sUtUTNUKsgL9AXVRnZCFZaR1DPIy4zP3iOfHxpCuFsLMFoFq2qC0LEGNPW7RgBcfGVKi%2BW9GbJLVsUMRZuyuASYwcbhUHl%2FkEi2fos%2B6%2FBndwgxOLqM1xa1Okd5sH1E4E1VvVxJAdu3p0z8kqk6y570xVZbp6TJL3zmkOI6RtAubfktzR0xv9CIC%2FyKSgz20uIHJ3r0nwKt6AWM%3D; _gat_gtag_UA_84556149_5=1',
        'origin': 'https://yoteshinportal.cc',
        'referer': ytsn_lk,
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62',
        'x-requested-with': 'XMLHttpRequest'
    }
    payload1 = {"key":"IcNF-SOBX"}
    req = session.post(sv_url,headers=headers1,json=payload1)
    info = req.content
    fileid = json.loads(info)['fileId']
    gdrv_lk = "https://drive.google.com/file/d/" + fileid
    return gdrv_lk
