import asyncio
from time import sleep
from aiogram import Bot, Dispatcher, executor, types
import logging
from cfg import get_admin_id, get_chat_id
from facebook_parser import facebookParsing
from telethon_parser import telegram_parser
import shutil
import os
from kb import main_bot_keyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import Database
from vk_parsing import vk_parsing_func
import configparser
from FSM import Groups, SetKeywords, DeleteKeywords, ParsingSettings
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
async def on_start_parsing(message, preset_name):
    currentChat = message.chat.id
    groupsList = db.make_array_from_groups_list(currentChat)
    while True:
        for group in groupsList:

            if group.split('/')[2] == 't.me':
                try:
                    result = await telegram_parser(group, preset_name)
                    for mess in result:
                        await bot.send_message(currentChat, f"{mess['message']}\nСсылка на пост: {mess['url']}")
                        await asyncio.sleep(5)
                        if mess['hasPhoto'] == True:
                            await bot.send_photo(currentChat, open(f'photos/{mess["messageName"]}.jpg', 'rb'))
                            await asyncio.sleep(5)
                    shutil.rmtree('photos')
                except:
                    continue


            elif group.split('/')[2] == 'vk.com':
                db.create_table(preset_name)
                try:

                    result = vk_parsing_func(group_name=group.split('/')[3], preset_name=preset_name)
                    if result['text'] not in db.make_array_from_post_content_data(preset_name):
                        db.insert_post_content(result['text'], preset_name)
                        await bot.send_message(currentChat, result['text'])

                        if result['photo'] is not None:
                            await bot.send_message(currentChat, result['photo'])
                except TypeError:
                    continue
                        
            elif group.split('/')[2] == 'facebook.com':
                pass
                # try:
                #     result = await facebookParsing(group, preset_name)
                #     for res in result:
                #         if res['image'] != 'Изображение отсутствует':
                #             await bot.send_message(currentChat, f"{res['text']}\n{res['link']}")
                #             for img in res['image']:
                #                 await bot.send_photo(currentChat, img)
                #                 await asyncio.sleep(2)
                            
                #         else:
                #             await bot.send_message(currentChat, f"{res['text']}\n{res['link']}")

                # except Exception as ex:
                #     print(ex)
                #     continue











#---------------------------START-----------------------------------------

@dp.message_handler(text='-Начать-парсинг✅')
async def startapp(message: types.Message):
    await ParsingSettings.preset_name.set()
    await bot.send_message(message.chat.id, 'Вывожу список ваших пресетов...')
    files = os.listdir('Keywords dir')
    for file in files:
        file_name = file.replace('.txt','')
        await bot.send_message(message.chat.id, file_name)
        sleep(1)
    await bot.send_message(message.chat.id, 'Введите имя выбранного пресета')

    

@dp.message_handler(state=ParsingSettings.preset_name)
async def start_parsing(message: types.Message, state=FSMContext):
    preset_name = message.text
    await state.finish()
    asyncio.create_task(on_start_parsing(message, preset_name=preset_name))

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
    await state.finish()




#---------------------------------DELETE GROUPS-------------------------------------------
@dp.message_handler(text='-Удалить список групп❌-')
async def handleDeleteGroups(message: types.Message):
    db.reset_groups_for_picked_channel(message.chat.id)
    await bot.send_message(message.chat.id, 'Группы успешно удаленны')



@dp.message_handler(text='==test==')
async def testFunc(message: types.Message):
    groupsList = db.make_array_from_groups_list(message.chat.id)
    chatId = message.chat.id
    userId = message.from_user.id
    await bot.send_message(chatId, f'groups:\n{groupsList}\nchat id:\n{chatId},\nuser id: {userId}')
    # await bot.send_message([chatId, -1001739302192], 'hello')
#-----------------------------ADD KEYWORDS--------------------------------------------------
@dp.message_handler(text='-Добавить ключевые слова🛠-', state=None)
async def add_keywords(message: types.Message):
    await SetKeywords.current_message.set()
    await bot.send_message(message.chat.id, 'Введите список ключевых слов через пробел (`квартира спальня гостинная`)')
@dp.message_handler(state=SetKeywords.current_message)
async def hanlde_keywords(message: types.Message, state=FSMContext):
    async with state.proxy() as sp:
        sp['keywords_list'] = message.text.lower().split()
    await SetKeywords.next()
    await bot.send_message(message.chat.id, 'Введите имя пресета ключевых слов')

@dp.message_handler(state = SetKeywords.preset_name)
async def preset_name_handle(message: types.Message, state=FSMContext):
    async with state.proxy() as sp:
        keywords_list = sp['keywords_list']
    preset_name = message.text
    with open(f'Keywords dir/{preset_name}.txt','a',encoding='utf-8') as f:
        for keyword in keywords_list:
            f.write(f'{keyword}\n')
    await bot.send_message(message.chat.id, f'Пресет с именем "{preset_name}" успешно создан')
    await state.finish()


#-----------------------------DELETE KEYWORDS-----------------------------------------------------


@dp.message_handler(text='-Удалить ключевые слова🚫-')
async def delete_keywords_preset(message: types.Message):
    await DeleteKeywords.preset_name.set()
    await bot.send_message(message.chat.id, 'Вывожу список ваших пресетов...')
    files = os.listdir('Keywords dir')
    for file in files:
        file_name = file.replace('.txt','')
        await bot.send_message(message.chat.id, file_name)
        sleep(1)
    await bot.send_message(message.chat.id, 'Введите пресета, который вы хотите удалить')
@dp.message_handler(state=DeleteKeywords.preset_name)
async def handle_preset_name_for_delete(message: types.Message, state=FSMContext):
    try:
        os.remove(f'Keywords dir/{message.text}.txt')
        await bot.send_message(message.chat.id,'Пресет успешно удален')
    except:
        await bot.send_message(message.chat.id,'Такого пресета не существует')
    finally:
        await state.finish()


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
