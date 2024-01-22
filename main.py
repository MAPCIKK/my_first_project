from telebot import *
import json
from plot import *
from telebot import types
from PIL import Image
img1 = Image.open('entrance.jpg').convert('RGB')
img2 = Image.open('passageway.jpg').convert('RGB')
img3 = Image.open('hall.jpg').convert('RGB')
img4 = Image.open('door.jpg').convert('RGB')
img5 = Image.open('hall.jpg').convert('RGB')
img6 = Image.open('hall.jpg').convert('RGB')
img7 = Image.open('bad_ending.jpg').convert('RGB')
img8 = Image.open('good_ending.jpg').convert('RGB')

photo = {
    1: img1,
    2: img2,
    3: img3,
    4: img4,
    5: img5,
    6: img6,
    7: img7,
    8: img8
}
token = input('Введите свой токен, выданный Bot_father')
bot = telebot.TeleBot(token)
user_id = 0
user_data = {

}

def find_value(dictionary, key):
    for dictionary_1 in dictionary.values():
        for dictionary_2 in dictionary_1.values():
            if type(dictionary_2) == dict:
                for k in dictionary_2.keys():
                    if k == key:
                        return dictionary_2[k]



def load_user_data(data_path):
    try:
        with open(data_path, 'r', encoding='utf8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_user_data(user_data, data_path):
    with open(data_path, 'w+', encoding='utf8') as file:
        json.dump(user_data, file, ensure_ascii=False)


file_path = 'user_data_file.json'


markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn3 = types.KeyboardButton("идти дальше")
markup2.add(btn3)

markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn5 = types.KeyboardButton("пойти к алтарю")
btn6 = types.KeyboardButton("пойти к колоннам")
markup3.add(btn5, btn6)

markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn8 = types.KeyboardButton("дверь с гравюрой")
btn9 = types.KeyboardButton("дверь с замком")
markup4.add(btn8, btn9)

markup5 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn11 = types.KeyboardButton("войти в потайной ход")
markup5.add(btn11)

markup6 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn13 = types.KeyboardButton("идти по карте")
btn14 = types.KeyboardButton("пойти к алтарю")
markup6.add(btn13, btn14)

markup7 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn15 = types.KeyboardButton("Еще раз?")
markup7.add(btn15)

markup8 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn16 = types.KeyboardButton("Еще раз?")
markup8.add(btn16)

markup9 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn16 = types.KeyboardButton("/start")
markup9.add(btn16)

markup = {
    2: markup2,
    3: markup3,
    4: markup4,
    5: markup5,
    6: markup6,
    7: markup7,
    8: markup8
}

@bot.message_handler(commands=['start'])
def start(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("пойти влево")
    btn2 = types.KeyboardButton("пойти вправо")
    markup1.add(btn1, btn2)
    user_data = load_user_data(file_path)
    user_id = str(message.from_user.id)
    bot.send_message(user_id,
                     'Добро пожаловать в бота-квест "В сердце пирамиды". Начинаем!'.format(
                         message.from_user), reply_markup=markup1)
    if str(user_id) not in user_data:
        user_data[user_id] = {'name': message.from_user.first_name,
                              'result': []}
        bot.send_photo(user_id, img1)
        bot.send_message(user_id, story[1]['description'])
        save_user_data(user_data, file_path)
    elif str(user_id) in user_data:
        user_result = user_data[user_id]['result']
        if user_result == []:
            bot.send_message(user_id, story[1]['description'])
            save_user_data(user_data, file_path)
        else:
            print("Что-то сломалось")

@bot.message_handler(content_types=['text'])
def handle_files(message):
    user_id = str(message.from_user.id)
    user_data = load_user_data(file_path)
    user_result = user_data[user_id]['result']
    if "еще раз?" in message.text.lower():
        user_data[user_id]['result'] = []
        bot.send_message(user_id, 'Нажмите /start когда будете готовы пройти тест заново. Если наигрались, просто покиньте дилог с ботом'.format(
                             message.from_user), reply_markup=markup9)
    else:
        try:
            question_number = find_value(story, message.text)
            button = markup[question_number]
            photo_number = photo[question_number]
            bot.send_photo(user_id, photo_number)
            bot.send_message(user_id, story[question_number]['description'].format(
                                 message.from_user), reply_markup=button)
            save_user_data(user_data, file_path)
        except KeyError:
            bot.send_message(user_id, 'Я Вас не понимаю'.format(
                             message.from_user), reply_markup=markup9)

bot.polling()