import requests
from configparser import ConfigParser
from data import get_words, get_kv_words
def vk_parsing_func(group_name, preset_name):
    config = ConfigParser()
    config.read('vk_config.ini')
    api_key = config['VK']['api_key']
    url = f'https://api.vk.com/method/wall.get?domain={group_name}&count=100&access_token={api_key}&v=5.131'
    req = requests.get(url)
    src = req.json()
    posts = src['response']['items']
    post_photo = []
    for post in posts:

        post_id = post["id"]

        try:
                
            post_text = post['text']
            splitted_text = post_text.lower().split()
            for keyword in get_words(preset_name):
                for kv_keyword in get_kv_words():
                    if keyword in splitted_text and kv_keyword in splitted_text:

                        if "attachments" in post:
                            post_attachments = post["attachments"]
                            # забираем фото
                            if post_attachments[0]["type"] == "photo":
                                photo_sizes = post_attachments[0]['photo']['sizes']
                                post_photo.append(photo_sizes[-1]['url'])
                        else:
                            post_photo = None
                            
                        return {
                            'text':post_text,
                            'photo':post_photo
                        }
                        
                    
        except Exception:
                print(f"Что-то пошло не так с постом ID {post_id}")

# print(vk_parsing_func('argentina_russia'))
