from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def plhh_gdrive(gdrv_lk):
    chrome_options = Options()
    chrome_options.addArguments("start-maximized")
    chrome_options.addArguments("disable-infobars")
    chrome_options.addArguments("--disable-extensions")
    chrome_options.addArguments("--disable-gpu")
    chrome_options.addArguments("--disable-dev-shm-usage")
    chrome_options.addArguments("--no-sandbox")
    #gdrv_lk = 'https://drive.google.com/file/d/1c7a1RTj9D0f7cLetIHtcUAZSizkT6iSi/view?usp=sharing'
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://publiclinks.hashhackers.com/")
    driveid = driver.find_element(By.XPATH, '//*[@id="driveid"]')
    driveid.click()
    driveid.send_keys(gdrv_lk)
    convert = driver.find_element(By.XPATH, '//*[@id="encrypt"]')
    convert.click()
    result = driver.find_element(By.XPATH, '//*[@id="result"]')
    my_link = result.get_attribute('value')
    driver.quit()
    return my_link

