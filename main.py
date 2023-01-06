import asyncio
from aiogram import Bot, Dispatcher, executor, types
import logging
from cfg import get_admin_id, get_chat_id
from facebook_parser import parsing
import os
import shutil
from kb import main_bot_keyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import Database
from vk_parsing import vk_parsing_func
import configparser
from asyncio.exceptions import TimeoutError
from telethon_parser import telegramParserMain
from FSM import Groups, DeleteGroups
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#Initializing
config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(level=logging.INFO)
Token = config['Telegram']['first_token']
admin_id = get_admin_id()
bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database('fb_db.db')

#--------------------------PARSING----------------------------------------
async def on_start_parsing(message: types.Message):
    curent_channel = await db.select_channel_id_by_group(message.chat.id)
    groups_list = await db.make_array_from_groups_list(message.chat.id)    
    while True:
        for i in groups_list:
            print(i)
            try:
                if i.split('/')[2] == 'vk.com':
                    res = await vk_parsing_func(i.split('/')[3])
                    if res['text'] not in db.make_array_from_post_content_data():
                        if res['photo'] != None:
                            await bot.send_message(message.chat.id, res['text'])
                            for img in res['photo']:
                                await bot.send_photo(message.chat.id, img)

                            await bot.send_message(curent_channel, res['text'])
                            for img in res['photo']:
                                await bot.send_photo(curent_channel, img)
                        else:
                            await bot.send_message(message.chat.id, res['text'])
                            await bot.send_message(curent_channel, res['text'])
                    else: 
                        continue
                elif i.split('/')[2] == 't.me':
                    result_list = telegramParserMain(i)
                    photo_iter = 1
                    for m in result_list:
                        await bot.send_message(message.chat.id, m) # сообщения
                        await bot.send_message(curent_channel, m)
                        
                        await bot.send_photo(message.chat.id, f'photos/{photo_iter}.jpg')
                        await bot.send_photo(curent_channel, f'photos/{photo_iter}.jpg')
                        photo_iter += 1
                    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'photos')
                    shutil.rmtree(path)
                elif i.split('/')[2] == 'facebook.com':
                    fb_groups = []
                    for fb_group in groups_list:
                        if fb_group.split('/')[2] == 'facebook.com':
                            fb_groups.append(fb_group)
                    result = await parsing(fb_groups)
                    for res in result:
                        if res != None:
                            if res['text'] not in db.make_array_from_post_content_data():
                                db.insert_post_content(res['text'])
                                caption = f'{res["text"]}\nСсылка:{res["link"]}'
                                caption_for_channel = f'{res["text"]}'
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
                            else:
                                continue
                        else:
                            continue

            except TimeoutError:
                continue
            except Exception as ex:
                print(ex)
    
#---------------------------START-----------------------------------------

@dp.message_handler(text='-Начать-парсинг✅')
async def startapp(message: types.Message):
    asyncio.run(await on_start_parsing(message))
    await bot.send_message(message.chat.id, 'Начало парсинга')
       

@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await bot.send_message(message.chat.id, 'Добро пожаловать! Воспользуйтесь клавиатурой или введите команды вручную!',reply_markup=main_bot_keyboard)


@dp.message_handler(text='-Помощь📃')
async def help_me(message: types.Message):
    await bot.send_message(message.chat.id, 'Вывожу клавиатуру', reply_markup=main_bot_keyboard)

#----------------------------------------GROUPS REGISTRATION-----------------------------------------
@dp.message_handler(text='-Зарегистрировать-группы📂', state=None)
async def register_groups(message: types.Message):
    await Groups.groups_list.set()
    await bot.send_message(message.chat.id, 'Введите список групп')    


@dp.message_handler(state=Groups.groups_list)
async def handle_groups_list(message: types.Message, state=FSMContext):
    db.add_new_list(message.chat.id, message.text)
    await Groups.next()
    await bot.send_message(message.chat.id, 'Введите id канала для парсинга')


@dp.message_handler(state=Groups.channel_id)
async def handle_channel_id(message:types.Message, state=FSMContext):
    db.add_new_channel_by_group(message.text, message.chat.id)
    await bot.send_message(message.chat.id, 'Регистрация прошла успешно')
    await state.finish()




#---------------------------------DELETE GROUPS-------------------------------------------
@dp.message_handler(text='-Удалить список групп❌-')
async def handleDeleteGroups(message: types.Message):
    db.reset_groups_for_picked_channel(message.chat.id)
    await bot.send_message(message.chat.id, 'Группы успешно удаленны')



@dp.message_handler(text='==test==')
async def testFunc(message: types.Message):
    groupsList = await db.make_array_from_groups_list(message.chat.id)
    chatId = message.chat.id
    userId = message.from_user.id
    await bot.send_message(chatId, f'groups:\n{groupsList}\nchat id:\n{chatId},\nuser id: {userId}')


#-----------------------------------COMMENTS-------------------------------------------------------------------
@dp.message_handler(content_types='text')
async def comments(message: types.Message):
    if message.from_user.id != int(admin_id):
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
