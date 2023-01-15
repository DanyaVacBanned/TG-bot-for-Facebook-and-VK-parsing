from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EX
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
db = Database('fb_db.db')



async def facebookParsing(url, name):
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
    for cookie in pickle.load(open('cookies_fb', 'rb')):
        driver.add_cookie(cookie)

    driver.refresh()
    await asyncio.sleep(2)
    print('Авторизация пройдена')
    print('Переход по ссылке..')
    driver.get(url=url)
    await asyncio.sleep(3)
    # try:
    #     driver.find_element(By.CSS_SELECTOR, 'div.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6.xlyipyv.xuxw1ft').click()
    # except:
    #     pass
    # try:
    #     accept_cookie = driver.find_element(By.CLASS_NAME,'_9xo7')
    #     accept_cookie.click()
    # except:
    #     pass
    # try:
    #     accept_license_button = driver.find_element(By.TAG_NAME,'button')
    #     accept_license_button.click()
    # except:
    #     pass
    # try:
    #     finall_button = driver.find_element(By.TAG_NAME,'button')
    #     finall_button.click()
    # except:
    #     pass
    # try:
    #     accept_all_cookies = driver.find_element(By.CSS_SELECTOR,'div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1iyjqo2.xs83m0k.x150jy0e.x1e558r4.xjkvuk6.x1iorvi4.xdl72j9')
    #     accept_all_cookies.click()
    # except:
    #     pass
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    await asyncio.sleep(10)
    driver.get_screenshot_as_file('fb_parser.png')
    
    divs = driver.find_elements(By.CLASS_NAME,'xquyuld')

    for words in divs[3:]:
        print('Поиск...')
        try:
            
            text_ = words.find_element(By.CLASS_NAME,'x1iorvi4')
            text_ = text_.text
            print(text_)
            await asyncio.sleep(5)
            splitted_text = text_.lower().split()
            print(splitted_text)
            if splitted_text[-1] == 'ещё':
                while splitted_text[-1] == 'ещё':
                    await asyncio.sleep(10)
                    more = words.find_element(By.CSS_SELECTOR,'div.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f')
                    await asyncio.sleep(10)
                    more.click()
                    await asyncio.sleep(5)
                    text_ = words.find_element(By.CLASS_NAME,'x1iorvi4').text #//*[@class="x1iorvi4 x1pi30zi x1l90r2v x1swvt13"]
                    splitted_text = text_.lower().split()
            print(text_)
            
        except Exception as ex:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            await asyncio.sleep(5)
            print(ex)
            continue
        
        for keyword in get_words(name):
            for kv_keyword in get_kv_words():
                if (keyword in splitted_text) and (kv_keyword in splitted_text) and (text_ not in db.make_array_from_post_content_data()):
                    db.insert_post_content(text_)
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
                    
    driver.close()
    driver.quit()
    return result_list


