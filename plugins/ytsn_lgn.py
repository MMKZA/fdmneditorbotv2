import requests
import json

async def ytsn_lgn(eml, pswd):
    url_login = 'https://yoteshinportal.cc/login'
    r = requests.session()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'content-length': '117',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': '_ga=GA1.2.197300883.1644724921; __gads=ID=482619c4e658619e:T=1658430248:S=ALNI_Ma1T3_FDX4ArBdB-_zkuvRhAv0ujQ; __gpi=UID=000007486aa5348d:T=1658430248:RT=1658430248:S=ALNI_MZ9O12EWFCVUPDiv11cumNXPj2Gag; _gid=GA1.2.2133751929.1658542817; _gat_gtag_UA_84556149_5=1; adonis-session=6e65c3420f269129ca60e5401cbc2741CIHopdkRpD3oARLZ3lqI5cndQPFjZdb%2B9rVUzLTbvCP%2F9sz7%2FNstU73mZjm5tTAAvGAWrIIemf0VM62%2BL6KE3Y2em%2FlC7YiYpxzuDjaXigysTKugmk%2FEpbjvx%2FLSFWVh; XSRF-TOKEN=8a71a0b1923451179b4a9b3229337fd9esg0aW04gTbwCNnm3Pu%2BUsjj5jhR5LBhEMffIAp%2FMBOCMF05LHLMpcjLGB%2FAEkrb2VyxmTtxkBxcyYQ0LmvGzuLkLyFdvvM%2F8Fm%2BXPu1eK%2FdPGtNB6t5kSUjrC8rQhBh; adonis-session-values=9327f1f52b79310054eb49e31ae61cd5o3931%2F2Zas7seAuZiROLm9%2BVDJOGcZIZViRQdcbLgZ0ZPCoTeRn9sLqnxmd6o48TQ%2FVh9QRB%2BCB%2BGYv3KgJRYxIAc%2FULLb5MQI%2FfWxUgd7LqWoReGy3hz9Un5gbOSVCKH96yH4XqUU5%2BQPKg%2B6X2vfXREGMkasiMxZjm3wFcyDmPXXR3keRFCBpbC8dFZwxtZM0PiSLjGpEZ8J7%2B9cFnjT%2FpL8hUMFjU8vkJvDNZWjbNM5gHSY%2B8QHncZEH2dII8VF%2BbQz85sS41cfM4WR6Hdcg81JOW8zOGk%2Fn9JLk0rd4%3D',
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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62'
        }
    payload = {
        '_csrf': 'CYBQBkYc-eZ8AqAz8WCg0h2bRkLFesdwuhuo',
        'username': eml,
        'password': pswd,
        'remember': 'true'
        }
    res = r.post(url_login,headers=headers,data=payload)
    return r
