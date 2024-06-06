import json
import os
import telebot
from telebot import types
bot = telebot.TeleBot('7230363856:AAEWb1BVKPeTgtw-ol-5rduEkGe_jJm5eVo')

def keyboard_generate(id, schema_id, node_list):
    keyboard = types.InlineKeyboardMarkup()
    for child in node_list[id]['childs']:
        data = f'{child} {schema_id}'
        button = types.InlineKeyboardButton(text=node_list[child]['label'], callback_data=data)
        keyboard.add(button)
    return keyboard


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/start':
        last_schema = len(os.listdir(path='Schemes'))
        print(last_schema)
        file = open(f'Schemes/schema{last_schema}.json', 'r', encoding='utf-8')
        node_list = json.load(file)
        file.close()
        start_id = str(min([int(i) for i in list(node_list.keys())]))
        # Создание меню с командами
        bot.set_my_commands(
            commands=[
                types.BotCommand('/start', 'Начать работу с ботом'),
            ],
            scope=types.BotCommandScopeChat(message.chat.id)
        )
        keyboard = keyboard_generate(start_id, last_schema, node_list)
        bot.send_message(message.from_user.id, text=node_list[start_id]['label'], reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, text='Неизвестная команда, введите /start для начала работы')


@bot.callback_query_handler(func=lambda call: True, )
def callback_worker(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    [ node_id, schema_id ] = call.data.split(' ')

    file = open(f'Schemes/schema{schema_id}.json', 'r', encoding='utf-8')
    node_list = json.load(file)
    file.close()

    if (len(node_list[node_id]['childs']) > 0):
        keyboard = keyboard_generate(node_list[node_id]['childs'][0], schema_id, node_list)
        bot.send_message(call.message.chat.id, text=node_list[node_list[node_id]['childs'][0]]['label'], reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, text=node_list[node_id]['label'])


bot.polling(none_stop=True, interval=0)