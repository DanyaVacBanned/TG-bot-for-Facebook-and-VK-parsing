
import asyncio
from data import get_words, get_kv_words
import pickle
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from database import Database
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
db = Database('fb_db.db')
async def parsing(url_list):
    ua = UserAgent()
    result_list = []
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument(f'User-Agent: {ua.random}')
    s = Service(executable_path='/home/tgbot/chromedriver')
    driver = webdriver.Chrome(service=s, options=options)
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
    driver.maximize_window()

    print('Идет авторизация...')
    driver.get('https://facebook.com')
    await asyncio.sleep(2)
    for cookie in pickle.load(open('cookies_boris_fb', 'rb')):
        driver.add_cookie(cookie)

    driver.refresh()
    await asyncio.sleep(2)
    print('Авторизация пройдена')
    for url in url_list:
        print('Переход по ссылке..')
        print(url)
        driver.get(url=url)
        await asyncio.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(5)
        driver.get_screenshot_as_file('async_parser.png')
        
        divs = driver.find_elements(By.CLASS_NAME,'xquyuld')

        
        for words in divs[2:]:
            print('Поиск...')
           

            try:
                more = words.find_element(By.CSS_SELECTOR,'div.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f')
                more.click()
            except:
                pass
            try:
                WebDriverWait(driver, timeout=10).until(driver.find_element(By.CLASS_NAME,'x1iorvi4'))
                text_ = words.find_element(By.CLASS_NAME,'x1iorvi4').text #//*[@class="x1iorvi4 x1pi30zi x1l90r2v x1swvt13"]
                splitted_text = text_.lower().split()
            except Exception as ex:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print(ex)
                continue
            
            for keyword in get_words():
                for kv_keyword in get_kv_words():
                    if keyword in splitted_text and kv_keyword in splitted_text:
                        try:
                            lnk = words.find_element(By.CLASS_NAME,'xaqea5y').get_attribute('href')
                        except NoSuchElementException:
                            lnk = 'Ссылка не найдена'

                        try:
                            pictures = words.find_elements(By.CSS_SELECTOR,'img.x1ey2m1c.xds687c.x5yr21d.x10l6tqk.x17qophe.x13vifvy.xh8yej3')
                            img = []
                            for pic in pictures:
                                img.append(pic.get_attribute('src'))
                        except NoSuchElementException:
                            img = 'Изображение отсутствует'
                        
                        result = {
                            'text':text_,
                            'link':lnk,
                            'image':img,
                            
                        }
                        result_list.append(result)
                        print(result_list)
    return result_list
