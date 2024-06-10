import telebot
from telebot import types

class Bot:
    def __init__(self, token, schema):
        self.bot = telebot.TeleBot(token)
        self.schema = schema

    def keyboard_generate(self, id, schema_id, node_list):
        print(id, schema_id, node_list)
        keyboard = types.InlineKeyboardMarkup()
        for child in node_list[id]['childs']:
            data = f'{child} {schema_id}'
            button = types.InlineKeyboardButton(text=node_list[child]['label'], callback_data=data)
            keyboard.add(button)
        return keyboard

    def start(self):
        @self.bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            if message.text == '/start':
                node_list = self.schema
                start_id = str(min([int(i) for i in list(node_list.keys())]))
                # Создание меню с командами
                self.bot.set_my_commands(
                    commands=[
                        types.BotCommand('/start', 'Начать работу с ботом'),
                    ],
                    scope=types.BotCommandScopeChat(message.chat.id)
                )
                print(start_id, 1, node_list)
                keyboard = self.keyboard_generate(start_id, 1, node_list)
                self.bot.send_message(message.from_user.id, text=node_list[start_id]['label'], reply_markup=keyboard)
            else:
                self.bot.send_message(message.from_user.id, text='Неизвестная команда, введите /start для начала работы')


        @self.bot.callback_query_handler(func=lambda call: True, )
        def callback_worker(call):
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
            [ node_id, schema_id ] = call.data.split(' ')

            node_list = self.schema

            if (len(node_list[node_id]['childs']) > 0):
                print(node_list[node_id]['childs'][0], schema_id, node_list)
                keyboard = self.keyboard_generate(node_list[node_id]['childs'][0], schema_id, node_list)
                self.bot.send_message(call.message.chat.id, text=node_list[node_list[node_id]['childs'][0]]['label'], reply_markup=keyboard)
            else:
                self.bot.send_message(call.message.chat.id, text=node_list[node_id]['label'])
        
        
        self.bot.polling()
    
    def change_schema(self, new_schema):
        self.schema = new_schema