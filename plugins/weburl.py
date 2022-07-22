from requests import post, get
# from requests_html import HTMLSession
from config import Config
import pyrogram
import requests
import re
from bs4 import BeautifulSoup
import logging
from trnl import Trnl
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from config import Config
import os

@pyrogram.Client.on_message(pyrogram.filters.regex(pattern=".*http.*"))
def trans(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        web_url = update.text
        Trnl.sh1.update('M2',web_url)
        if "https://goldchannel.net/movies/" in web_url:
            web_req = requests.get(web_url)
            # override encoding by real educated guess as provided by chardet
            web_req.encoding = web_req.apparent_encoding
            # access the data
            web_html = web_req.text
            soup = BeautifulSoup(web_html, 'html.parser')
            urls_lst = []
            for a in soup.find_all('a', href=True):
                urls_lst.append(a['href'])
            url_lst = [x for x in urls_lst if x.startswith('https://goldchannel.net/links/')]
            sizes_lst = []
            for a in soup.find_all("strong", {"class": "quality"}):
                sizes_lst.append(a.text)
            table = ''
            for a in soup.find_all('div', {'class': 'links_table'}):
                table = a.text
            sttrm1080 = 'G Drive FHD 1080pMyanmar'
            sttrm720 = 'G Drive HD 720pMyanmar'
            sttrm480 = 'G Drive SD 480pMyanmar'
            entrmGB = ' GB'
            entrmMB = ' MB'
            sz_lst = []
            if sttrm1080 in table:
                if entrmGB in table:
                    size1080 = (table.split(sttrm1080))[1].split(entrmGB)[0]
                    if "Myanmar" in size1080:
                        size1080 = "{:.2f}".format(float((table.split(sttrm1080))[1].split(entrmMB)[0]) / 1024)
                    else:
                        size1080 = float(size1080)
                    sz_lst.append(float(size1080))
            if sttrm720 in table:
                if entrmGB in table:
                    size720 = (table.split(sttrm720))[1].split(entrmGB)[0]
                    if "Myanmar" in size720:
                        size720 = "{:.2f}".format(float((table.split(sttrm720))[1].split(entrmMB)[0]) / 1024)
                    else:
                        size720 = float(size720)
                    sz_lst.append(float(size720))
            if sttrm480 in table:
                size480 = "{:.2f}".format(float((table.split(sttrm480))[1].split(entrmMB)[0]) / 1024)
                sz_lst.append(float(size480))
            a = list(range(0, len(sizes_lst)))
            chs_lst = list(range(0, len(sizes_lst)))
            chss_lst = list(range(0, len(sizes_lst)))
            for i in a:
                chs_lst[i] = url_lst[i] + " | " + sizes_lst[i]
            for i in a:
                if "1080" in chs_lst[i]:
                    chss_lst[i] = chs_lst[i] + " | " + str(size1080) + "GB"
                if "720" in chs_lst[i]:
                    chss_lst[i] = chs_lst[i] + " | " + str(size720) + "GB"
                if "480" in chs_lst[i]:
                    chss_lst[i] = chs_lst[i] + " | " + str(size480) + "GB"

            gdrv_1080 = ''
            gdrv_720 = ''
            gdrv_480 = ''
            gold_lk = ''
            for a in chss_lst:
                if "G Drive FHD 1080p" in a:
                    gdrv_1080 = list(filter(lambda x: "G Drive FHD 1080p" in x, chss_lst))
                    lk_1080 = re.search("(?P<url>https?://[^\s]+)", gdrv_1080[0]).group("url")
                if "G Drive HD 720p" in a:
                    gdrv_720 = list(filter(lambda x: "G Drive HD 720p" in x, chss_lst))
                    lk_720 = re.search("(?P<url>https?://[^\s]+)", gdrv_720[0]).group("url")
                if "G Drive SD 480p" in a:
                    gdrv_480 = list(filter(lambda x: "G Drive SD 480p" in x, chss_lst))
                    lk_480 = re.search("(?P<url>https?://[^\s]+)", gdrv_480[0]).group("url")
            indices = [v for i, v in enumerate(sz_lst) if v < 2]
            max_sz = max(indices)
            for a in chss_lst:
                if "G Drive FHD 1080p" in a:
                    if max_sz == float(size1080):
                        gold_lk = lk_1080
                if "G Drive HD 720p" in a:
                    if max_sz == float(size720):
                        gold_lk = lk_720
                if "G Drive SD 480p" in a:
                    if max_sz == float(size480):
                        gold_lk = lk_480
            gold_req = requests.get(gold_lk)
            gold_req.encoding = gold_req.apparent_encoding
            gold_html = gold_req.text
            soup = BeautifulSoup(gold_html, 'html.parser')
            gold_lsts = []
            for a in soup.find_all('a', href=True):
                gold_lsts.append(a['href'])
            gdrv_lk = [x for x in gold_lsts if x.startswith('https://drive.google.com/file/d/')][0]
            bot.send_message(
                chat_id=update.chat.id,
                text=gdrv_lk
            )
            base = Trnl.sh1.acell('K2').value
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
                link=gdrv_lk,
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
            Trnl.sh1.update('L2', final_link)
            bot.send_message(
                chat_id=update.chat.id,
                text="Link မှန်ကန်ပါက ဇာတ်ကားတင်လို့ရပါပြီ 👇\n" + final_link
            )
        if "https://channelmyanmar.org/" in web_url:
            web_req = requests.get(web_url)
            # override encoding by real educated guess as provided by chardet
            web_req.encoding = web_req.apparent_encoding
            # access the data
            web_html = web_req.text
            soup = BeautifulSoup(web_html, 'html.parser')
            urls_lst = []
            url_lst = []
            for a in soup.find_all('li', {'class': 'elemento'}):
                urls_lst.append(a)
            url_cmb = ''.join(map(str, urls_lst))
            soup = BeautifulSoup(url_cmb, 'html.parser')
            for a in soup.find_all('a', href=True):
                url_lst.append(a['href'])
            qlt_lst = []
            for a in soup.find_all('span', {'class': 'd'}):
                qlt_lst.append(a.text)
            szs_lst = []
            for a in soup.find_all('span', {'class': 'c'}):
                szs_lst.append(a.text)
            sz_lst = list(range(0, len(szs_lst)))
            a = list(range(1, len(szs_lst)))
            chss_lst = list(range(0, len(szs_lst)))
            for i in chss_lst:
                chss_lst[i] = url_lst[i] + " | " + qlt_lst[i] + " | " + szs_lst[i]
            cnmm_lst = list(filter(lambda x: "https://yoteshinportal.cc/" in x, chss_lst))
            for a in qlt_lst:
                if "1080" in a:
                    kwd_1080 = list(filter(lambda x: "1080" in x, qlt_lst))[0]
                    cnmm_1080 = list(filter(lambda x: kwd_1080 in x, cnmm_lst))
                    spl_1080 = " | " + kwd_1080 + " | "
                    lk_1080 = re.search("(?P<url>https?://[^\s]+)", cnmm_1080[0]).group("url")
                    szstr_1080 = (cnmm_1080[0].split(spl_1080))[1]
                    if "GB" in szstr_1080:
                        sz_1080 = float(szstr_1080.replace("GB", "").strip())
                    if "MB" in szstr_1080:
                        sz_1080 = "{:.2f}".format(float(szstr_1080.replace("MB", "").strip()) / 1024)
            for a in qlt_lst:
                if "720" in a:
                    kwd_720 = list(filter(lambda x: "720" in x, qlt_lst))[0]
                    cnmm_720 = list(filter(lambda x: kwd_720 in x, cnmm_lst))
                    spl_720 = " | " + kwd_720 + " | "
                    lk_720 = re.search("(?P<url>https?://[^\s]+)", cnmm_720[0]).group("url")
                    szstr_720 = (cnmm_720[0].split(spl_720))[1]
                    if "GB" in szstr_720:
                        sz_720 = float((cnmm_720[0].split(spl_720))[1].replace("GB", "").strip())
                    if "MB" in szstr_720:
                        sz_720 = "{:.2f}".format(
                            float((cnmm_720[0].split(spl_720))[1].replace("MB", "").strip()) / 1024)
            for a in qlt_lst:
                if "480" in a:
                    kwd_480 = list(filter(lambda x: "480" in x, qlt_lst))[0]
                    cnmm_480 = list(filter(lambda x: kwd_480 in x, cnmm_lst))
                    spl_480 = " | " + kwd_480 + " | "
                    lk_480 = re.search("(?P<url>https?://[^\s]+)", cnmm_480[0]).group("url")
                    szstr_480 = (cnmm_480[0].split(spl_480))[1]
                    if "GB" in szstr_480:
                        sz_480 = float(szstr_480.replace("GB", "").strip())
                    if "MB" in szstr_480:
                        sz_480 = "{:.2f}".format(float(szstr_480.replace("MB", "").strip()) / 1024)
            arr = list(range(0, len(szs_lst)))
            a = list(range(0, len(szs_lst)))
            for i in a:
                if "GB" in szs_lst[i]:
                    arr[i] = float(szs_lst[i].replace("GB", "").strip())
                if "MB" in szs_lst[i]:
                    arr[i] = float("{:.2f}".format(float(szs_lst[i].replace("MB", "").strip()) / 1024))
            indices = [v for i, v in enumerate(arr) if v < 2]
            max_sz = max(indices)
            for a in cnmm_lst:
                if "1080" in a:
                    if max_sz == float(sz_1080):
                        gdrv_lk = lk_1080
                if "720" in a:
                    if max_sz == float(sz_720):
                        gdrv_lk = lk_720
                if "480" in a:
                    if max_sz == float(sz_480):
                        gdrv_lk = lk_480
            bot.send_message(
                chat_id=update.chat.id,
                text=gdrv_lk
            )
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
                                      chrome_options=chrome_options)
            url = gdrv_lk
            driver.get(url)
            time.sleep(1)
            popup = driver.find_element(By.XPATH, '/html/body/section[2]/style')
            driver.execute_script("""
                    var popup = arguments[0];
                    popup.parentNode.removeChild(popup);
                    """, popup)
            login_btn = driver.find_element(By.XPATH,
                                            '/html/body/section[2]/div[1]/div[2]/div/div[1]/div[3]/div/div[3]/div/a')
            time.sleep(1)
            login_btn.click()
            email = driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div[3]/input")
            email.click()
            email.send_keys('robertfalconscott1997@gmail.com')
            email = driver.find_element(By.CSS_SELECTOR,
                                        "body > div > div > div > div > form > div.input-group.flex-nowrap.mb-2 > input")
            email.click()
            email.send_keys('Vending5')
            sbmt_lgn = driver.find_element(By.XPATH, '/html/body/div/div/div/div/form/button')
            sbmt_lgn.click()
            popup = driver.find_element(By.XPATH, '/html/body/section[2]/style')
            driver.execute_script("""
                    var popup = arguments[0];
                    popup.parentNode.removeChild(popup);
                    """, popup)
            time.sleep(10)
            sgd_btn = driver.find_element(By.XPATH, '//*[@id="button-text"]/i')
            sgd_btn.click()
            dwnl_btn = driver.find_element(By.XPATH, '//*[@id="countdown"]')
            time.sleep(2)
            dwnl_btn.click()
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[1])
            last_url = driver.current_url
            driver.delete_all_cookies()
            base = Trnl.sh1.acell('K2').value
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
            Trnl.sh1.update('L2', final_link)
            bot.send_message(
                chat_id=update.chat.id,
                text="Link မှန်ကန်ပါက ဇာတ်ကားတင်လို့ရပါပြီ 👇\n" + final_link
            )
