from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def plhh_gdrive(gdrv_lk):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path='/app/.chromedriver/bin/chromedriver',chrome_options=options)
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

