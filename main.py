from aiogram import Bot, Dispatcher, executor, types
import logging
from cfg import get_token, get_admin_id, get_chat_id, tmp
from parseFile import parsing, get_urls
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from FSM import Groups
#Initializing
logging.basicConfig(level=logging.INFO)
Token = get_token()
storage = MemoryStorage()
admin_id = get_admin_id()
bot = Bot(token=Token)
dp = Dispatcher(bot, storage=storage)

#BODY

@dp.message_handler(commands=['fb_parse'])
async def on_start(message: types.Message):
    await bot.send_message(message.chat.id, 'Привет! Начинаю работу...')
    for i in get_urls():
        res = str(parsing(i))
        if res != 'None':
            await bot.send_message(message.chat.id, res)
    

@dp.message_handler(commands=['get_id'])
async def get_my_chat(message: types.Message):
    await bot.send_message(message.chat.id, message.chat.id)

@dp.message_handler(commands=['reg'], state=None)
async def get_start(message: types.Message):
    print('Бот отреагировал на сообщение')
    await Groups.groups.set()
    await bot.send_message(message.chat.id, 'Введите список групп: ')
@dp.message_handler(state=Groups.groups)
async def load_groups(message: types.Message, state=FSMContext):
    async with state.proxy() as sp:
        sp['groups'] = message.text
        await Groups.next()
        await bot.send_message(message.chat.id, "Введите код страны в двоичном формате (ru, us, de)")
@dp.message_handler(state=Groups.country)
async def load_country(message: types.Message, state=FSMContext):
    async with state.proxy() as sp:
        country = message.text
        groups = sp['groups']
        with open(f'groups/groups_{country}.txt', 'w', encoding='utf-8') as f:
            f.write(groups)
        tmp(message.text)
    await state.finish()
        

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
#----------------------------------------------------------------------------
#States

if __name__ =='__main__':
    executor.start_polling(dp, skip_updates=True)

    #id = 108 gid = 113