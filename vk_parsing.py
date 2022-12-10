
from time import sleep
from selenium import webdriver
from data import get_words, get_kv_words
from selenium.webdriver.firefox.options import Options
import pickle
from fake_useragent import UserAgent

def vk_parsing_func(url):
    ua = UserAgent()
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.set_preference('dom.webdriver.enabled', False)
    options.set_preference('dom.webnotifications.enabled', False)
    options.set_preference('dom.volume_scale', '0.0')
    options.add_argument(f'User-Agent: {ua.random}')
    driver = webdriver.Firefox(executable_path='/home/tgbot/geckodriver', options=options)
    driver.maximize_window()
    #Autoriazation
    print('Идёт авторизация..')
    driver.get('https://vk.com')
    sleep(5)
    for cookie in pickle.load(open('cookies_vk_new', 'rb')):
        driver.add_cookie(cookie)
    sleep(5)
    driver.refresh()
    sleep(5)
    print('Авторизация пройдена')
    print('Переход по ссылке..')
    driver.get(url=url)
    sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(5)
    print('Поиск...')
    divs = driver.find_elements_by_class_name('_post_content')
    driver.get_screenshot_as_file('vk_image.png')
    for words in divs:
        try:
            more_btn = words.find_element_by_class_name('PostTextMore__content')
            more_btn.click()
        except:
            pass
        text = words.find_element_by_class_name('wall_post_text').text
        splitted_text = text.lower().split()
        for keyword in get_words():
            for kv_keyword in get_kv_words():
                if keyword in splitted_text and kv_keyword in splitted_text():
                    try:
                        images = []
                        imgs = words.find_elements_by_class_name('MediaGrid__imageSingle')
                        for img in imgs:
                            images.append(img.get_attribure('src'))
                    except:
                        images = 'Изображения не найденны'
                    result = {
                        'text':text,
                        'images':images,
                        'url':url,
                    }
                    return result
