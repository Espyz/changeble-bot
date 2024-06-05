import json
import sys
import telebot
from telebot import types
bot = telebot.TeleBot('7230363856:AAEWb1BVKPeTgtw-ol-5rduEkGe_jJm5eVo')

node_list = {}
start_id = str(sys.maxsize * 2 + 1)

def keyboard_generate(id):
    keyboard = types.InlineKeyboardMarkup()
    for child in node_list[id]['childs']:
        button = types.InlineKeyboardButton(text=node_list[child]['label'], callback_data=child)
        keyboard.add(button)
    return keyboard


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global node_list
    if message.text == '/start':
        file = open('schemes.json', 'r', encoding='utf-8')
        node_list = json.load(file)
        file.close()
        start_id = min(list(node_list.keys()))
        print(node_list)
        # Создание меню с командами
        bot.set_my_commands(
            commands=[
                types.BotCommand('/start', 'Начать работу с ботом'),
            ],
            scope=types.BotCommandScopeChat(message.chat.id)
        )
        keyboard = keyboard_generate(start_id)
        bot.send_message(message.from_user.id, text=node_list[start_id]['label'], reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, text='Неизвестная команда, введите /start для начала работы')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if (len(node_list[call.data]['childs']) > 0):
        keyboard = keyboard_generate(node_list[call.data]['childs'][0])
        bot.send_message(call.message.chat.id, text=node_list[node_list[call.data]['childs'][0]]['label'], reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, text=node_list[call.data]['label'])


bot.polling(none_stop=True, interval=0)