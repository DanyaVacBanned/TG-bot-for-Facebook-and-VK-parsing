from telethon.sync import TelegramClient
from configparser import ConfigParser
from telethon.tl.functions.messages import GetHistoryRequest
from database import Database
import asyncio
from data import get_words, get_kv_words
import random
import string
async def telegram_parser(url, preset_name):
    loop = asyncio.new_event_loop()
    db = Database('fb_db.db')
    messageName = ''
    config = ConfigParser()
    config.read('telegram_config.ini')
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    client = TelegramClient('+79674699128', api_id=api_id, api_hash=api_hash, loop = loop)
    async with client:
        target_group = url
        offset_id = 0
        limit = 100
        total_messages = 0
        total_count_limit = 5
        all_messages = []
        num = 0
        while True:
            history = await client(GetHistoryRequest(
                peer=target_group,
                offset_id=offset_id,
                limit=limit,
                offset_date=None,
                add_offset = 0,
                max_id = 0,
                min_id = 0,
                hash = 0
            ))
            if not history.messages:
                break
            messages = history.messages
            for message in messages:
                hasPhoto = False
                try:
                    stripped_message = message.message.strip().lower().split()
                except:
                    continue
                for keyword in get_words(preset_name):
                    for kv_keyword in get_kv_words():
                        if (keyword in stripped_message) and (kv_keyword in stripped_message) and (message.message not in db.make_array_from_post_content_data()):
                            messageName = randomNameGen()
                            if message.photo:
                                await client.download_media(message,f'photos/{messageName}.jpg')
                                hasPhoto = True
                            db.insert_post_content(message.message)
                            all_messages.append(
                                {
                                    'message':message.message,
                                    'messageName':messageName,
                                    'hasPhoto':hasPhoto
                                }
                            )
            
            offset_id = messages[len(messages)-1].id
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
        return all_messages
    



def randomNameGen():
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(10))
    return result

 


