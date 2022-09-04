from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

def plhh_gdrive(gdrv_lk):
    #gdrv_lk = 'https://drive.google.com/file/d/1c7a1RTj9D0f7cLetIHtcUAZSizkT6iSi/view?usp=sharing'
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)
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

