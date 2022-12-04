from time import sleep
from aiogram import Bot, Dispatcher, executor, types
import logging
from cfg import get_admin_id, get_chat_id, get_channel_id
from parseFile import parsing
from kb import main_bot_keyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import Database
# from vk_parsing import vk_parsing_func
import configparser
from asyncio.exceptions import TimeoutError
import asyncio
#Initializing
config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(level=logging.INFO)
Token = config['Telegram']['first_token']
admin_id = get_admin_id()
bot = Bot(token=Token)
dp = Dispatcher(bot)
db = Database('fb_db.db')

#--------------------------PARSING----------------------------------------


@dp.message_handler(commands=['Начало_парсинга'])
async def on_start_parsing(message: types.Message):
    fb_posts = []
    
    try:
        await bot.send_message(message.chat.id, 'Привет! Начинаю работу...')
        for i in db.make_array_from_groups_list(message.chat.id):
            curent_channel = db.select_channel_id_by_group(message.chat.id)
            if i.split('/')[2] == 'facebook.com':
                print('Начало парсинга')
                res = parsing(i)
                print(res)
                if res != None:
                    if res['text'] not in fb_posts:
                        caption = f'Есть совпадение по слову {res["keyword"]}:\n{res["text"]}\nнайденно в группе:{res["group"]},\nЛокация: {res["place"]}\nСсылка:{res["link"]}'
                        caption_for_channel = f'{res["text"]}\n\nЛокация: {res["place"]}'
                        fb_posts.append(res['text'])
                        if res['image'] != 'Изображение отсутствует':
                            try:
                                await bot.send_message(message.chat.id,text=caption)
                                await bot.send_message(curent_channel,text=caption_for_channel)
                                for pic in res['image']:
                                    await bot.send_photo(message.chat.id, pic)
                                    await bot.send_photo(curent_channel, pic)
                            except:
                                await bot.send_message(message.chat.id,text=caption)
                                await bot.send_message(curent_channel,text=caption_for_channel)
                        else:
                            await bot.send_message(message.chat.id, text=caption)
                            await bot.send_message(curent_channel,text=caption_for_channel)
        

            
                # elif i.split('/')[2] == 'vk.com':
                #     if message.chat.type == "private":
                #         res = vk_parsing_func(i)
                #         if res != None:
                #             try:
                #                 await bot.send_photo(message.chat.id, f"{res['img']}")
                #                 await bot.send_message(message.chat.id, f"{res['text']} \n {res['link']}")
                #             except:
                #                 await bot.send_message(message.chat.id, f"{res['text']} \n {res['link']}")
                #     else:
                #         res = vk_parsing_func(i)
                #         if res != None:
                #             try:
                #                 await bot.send_photo(get_channel_id(), f"{res['img']}")
                #                 await bot.send_message(get_channel_id(), f"{res['text']}")
                #             except:
                #                 await bot.send_message(get_channel_id(), f"{res['text']}")

                # else:
                #     await bot.send_message(message.chat.id, 'Ссылка указана неверно')
                    else:
                        await bot.send_message(message.chat.id, 'Ничего не найденно')
    except TimeoutError:
        pass

#---------------------------START-----------------------------------------

@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await bot.send_message(message.chat.id, text='Здравствуйте!, чтобы зарегистрировать группы, перейдите по этой ссылке: {link}', reply_markup=main_bot_keyboard)
    
#----------------------------GET CURRENT CHAT ID--------------------------
@dp.message_handler(commands=['Получить_ID'])
async def get_my_chat(message: types.Message):
    await bot.send_message(message.chat.id, message.chat.id)  # type: ignore

    
#-----------------------------------COMMENTS-------------------------------------------------------------------
@dp.message_handler(content_types='text')
async def comments(message: types.Message):
    if message.text != '/get_id' and message.text != '/fb_parse' and message.text != '/start' and message.text != '/reg': 
        for chat_id in get_chat_id():
            
            
            if str(message.chat.id) == str(chat_id):
                link = await bot.create_chat_invite_link(message.chat.id)
                kb_btn = InlineKeyboardButton(text='Посмотреть комментарий', url=link['invite_link'])
                kb = InlineKeyboardMarkup()
                kb.add(kb_btn)

                await bot.send_message(admin_id, 'У вас новый комментарий!\n'+message.text, reply_markup=kb)



    




if __name__ =='__main__':
    executor.start_polling(dp, skip_updates=True)

    #id = 108 gid = 113
