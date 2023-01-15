from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_button = KeyboardButton('-Помощь📃')
parsing_button = KeyboardButton('-Начать-парсинг✅')
reg_groups_btn = KeyboardButton('-Зарегистрировать-группы📂')
delete_groups_btn = KeyboardButton('-Удалить список групп❌-')
add_keyword_btn = KeyboardButton('-Добавить ключевые слова🛠-')
delete_keyword_btn = KeyboardButton('-Удалить ключевые слова🚫-')


main_bot_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_bot_keyboard.add(start_button).add(parsing_button).add(reg_groups_btn).add(delete_groups_btn).add(add_keyword_btn).add(delete_keyword_btn)


