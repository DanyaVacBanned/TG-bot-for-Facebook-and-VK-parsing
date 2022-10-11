from random import choice
import re
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup as b
from data import get_words
from selenium.webdriver.firefox.options import Options
import pickle
from cfg import tmp_get

def get_urls():
    with open(f'groups/groups_{tmp_get()}.txt', 'r', encoding='utf-8') as f:
        array = [row.strip() for row in f]
        return array

def parsing(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.set_preference('dom.webdriver.enabled', False)
    options.set_preference('dom.webnotifications.enabled', False)
    options.set_preference('dom.volume_scale', '0.0')
    options.add_argument(str(random_headers()))
    driver = webdriver.Firefox(executable_path='/home/tgbot/geckodriver', options=options)
    driver.maximize_window()
    #Autoriazation
    print('Идёт авторизация..')
    driver.get('https://facebook.com')
    sleep(10)
    for cookie in pickle.load(open('cookies_firefox', 'rb')):
        driver.add_cookie(cookie)
    sleep(5)
    driver.refresh()
    sleep(10)

    print('Авторизация пройдена')
    print('Переход по ссылке..')

    driver.get(url=url)
    sleep(20)
    driver.execute_script("window.scrollTo(0, 1200)")
    sleep(10) 
    page = driver.page_source
    soup = b(page, 'lxml') 
    sleep(10)
    divs = soup.find_all('div',class_='bdao358l')
    print('Поиск..')
    for word in soup.get_text().lower().split():
        for div in divs:
            for keyword in get_words():
                if word == keyword:
                    print('Бот зашёл в if')
                    full_text = div.find(text=re.compile(keyword))
                    lnk = url
                    returned = f'Есть совпадение: по слову `{keyword}` найденно:\n{full_text}\nв группе {lnk}'
                    driver.quit()
                    return returned

                    


def random_headers():
    desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
                            

