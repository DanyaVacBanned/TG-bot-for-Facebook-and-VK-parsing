
from random import choice
from time import sleep
from selenium import webdriver
from data import get_words, get_kv_words
from selenium.webdriver.firefox.options import Options
import pickle
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
    sleep(5)
    for cookie in pickle.load(open('cookies_boris_fb', 'rb')):
        driver.add_cookie(cookie)
    sleep(5)
    driver.refresh()
    sleep(5)
    print('Авторизация пройдена')
    print('Переход по ссылке..')
    driver.get(url=url)
    try:
        accept_cookie = driver.find_element_by_class_name('_9xo7')
        accept_cookie.click()
    except:
        pass
    try:
        accept_license_button = driver.find_element_by_tag_name('button')
        accept_license_button.click()
    except:
        pass
    try:
        finall_button = driver.find_element_by_tag_name('button')
        finall_button.click()
    except:
        pass
    try:
        accept_all_cookies = driver.find_element_by_css_selector('div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1iyjqo2.xs83m0k.x150jy0e.x1e558r4.xjkvuk6.x1iorvi4.xdl72j9')
        accept_all_cookies.click()
    except:
        pass
    sleep(20)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(5)
    print('Поиск...')
    divs = driver.find_elements_by_class_name('xquyuld')
    driver.get_screenshot_as_file('image.png')
    
    sleep(5)
    
    
    for words in divs[2:]:
                                    
                               
        try:                                               
            try:                                            
                more = words.find_element_by_css_selector('div.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f')
                sleep(5)                                   
                more.click()
            except:
                pass
            text_ = words.find_element_by_class_name('x1iorvi4').text
            splitted_text = text_.lower().split()
            print(text_)
        except:
            continue
        for keyword in get_words():
            for kv_keyword in get_kv_words():
                if keyword in splitted_text and kv_keyword in splitted_text:                
                    try:
                        lnk = words.find_element_by_class_name('xaqea5y').get_attribute('href')
                    except:
                        lnk = 'Ссылка не найдена'
                    try:
                        pictrue = words.find_elements_by_css_selector('img.x1ey2m1c.xds687c.x5yr21d.x10l6tqk.x17qophe.x13vifvy.xh8yej3')
                        img = []
                        for pic in pictrue:
                            img.append(pic.get_attribute('src'))
                    except:
                        img = 'Изображение отсутствует' 
                    try:
                        try:
                            place = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div/div/div/div[2]/div[4]/div/div/div[2]/div/div/div/div/span').text.strip()
                        except:
                            place = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div/div[2]/div[4]/div/div/div[2]/div/div/div/div/span').text.strip()
                    

                    except Exception as ex:
                        print(ex)
                        place = 'Местоположение не указанно'


                    try:
                        pick_on_post = words.find_element_by_css_selector('img.x1ey2m1c.xds687c.x5yr21d.x10l6tqk.x17qophe.x13vifvy.xh8yej3')
                        pick_on_post.click()
                        sleep(5)
                        link_on_post = driver.current_url
                    except:
                        link_on_post = url
                            
                    if place == 'Местоположение не указанно':
                        result = {
                            'text':text_,
                            'link':lnk,
                            'image':img,
                            'keyword':keyword,
                            'place': place,
                            'group': link_on_post
                            }
                        driver.quit()
                        return result
                    else:
                        result = {
                            'text':text_,
                            'link':lnk,
                            'image':img,
                            'keyword':keyword,
                            'place':'https://www.google.ru/maps/place/'+place.replace(' ', ''),
                            'group':link_on_post
                        }
                        
                        driver.quit()
                        return result

                

        
                    


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

# print(parsing('https://facebook.com/groups/464178307448792?group_view_referrer=search'))
