import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pickle
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox()
driver.get('https://web.telegram.org/k/')
# input()
# pickle.dump(driver.get_cookies(), open('cookies_vk', 'wb'))
# time.sleep(2)

for cookie in pickle.load(open('cookies_telegram', 'rb')):
    driver.add_cookie(cookie)
time.sleep(5)
driver.refresh()
time.sleep(5)
input()
driver.close()
driver.quit()