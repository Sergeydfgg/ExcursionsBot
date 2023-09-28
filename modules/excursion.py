import telebot
import os
import media_from_bot
from telebot import types

TOKEN = os.getenv("TG_TOKEN")
tb = telebot.TeleBot(TOKEN)


class StackOfPath:
    def __init__(self):
        self.places_dict = {}
        self.song_dict = {}

    def add_new_list(self, path_key, places_path):
        self.places_dict.update({path_key: places_path})

    def add_new_song_list(self, path_key, list_of_songs):
        self.song_dict.update({path_key: list_of_songs})

    def set_new_place(self, path_key, new_line):
        self.places_dict[path_key].append(new_line)

    def set_new_song(self, path_key, new_song):
        self.song_dict[path_key].append(new_song)

    def delete_places_path(self, path_key):
        self.places_dict.pop(path_key)

    def delete_song_list(self, path_key):
        self.song_dict.pop(path_key)

    def show_places_in_list(self, path_key):
        print(self.places_dict[path_key])
        print(self.song_dict[path_key])


def place_control_sum(place_name: str) -> int:
    control_sum = 0
    for i in place_name:
        control_sum += ord(i)
    return control_sum


availabe_places = {place_control_sum('Первое место'): 'Первое место',
                   place_control_sum('Второе место'): 'Второе место',
                   place_control_sum('Третье место'): 'Третье место'}


availabe_songs = {place_control_sum('трах-трах'): 'трах-трах',
                  place_control_sum('Дядя не надо'): 'Дядя не надо'}


pathes_of_users = StackOfPath()


path_one_lib_media = ['C:/Users/Сергей/PycharmProjects/python_bot_project/documents/ass.docx',
                      'C:/Users/Сергей/PycharmProjects/python_bot_project/documents/kish.docx',
                      'C:/Users/Сергей/PycharmProjects/python_bot_project/documents/jel.docx',
                      'C:/Users/Сергей/PycharmProjects/python_bot_project/documents/pish.docx',
                      'C:/Users/Сергей/PycharmProjects/python_bot_project/documents/rot.docx']

path_one_lib_audio = ['C:/Users/Сергей/PycharmProjects/python_bot_project/audio/piz.mp3',
                      'C:/Users/Сергей/PycharmProjects/python_bot_project/audio/nenado.mp3',
                      'C:/Users/Сергей/PycharmProjects/python_bot_project/audio/good.mp3',
                      'C:/Users/Сергей/PycharmProjects/python_bot_project/audio/breath.mp3',
                      'C:/Users/Сергей/PycharmProjects/python_bot_project/audio/aaa.mp3']

path_one_points = ['Идите в Жопу, вот координаты: 44.46885, 33.63785',
                   'Идите в Прямую кишку, вот координаты: 59.46885, 63.63785',
                   'Идите в Желудок, вот координаты: 44.46885, 33.63785',
                   'Идите в Пищевод, вот координаты: 44.46885, 33.63785',
                   'Идите в Рот, вот координаты: 44.46885, 33.63785']


def path_choice(message):
    keyboard = types.InlineKeyboardMarkup()
    key_path1 = types.InlineKeyboardButton(text='Первый маршрут', callback_data='one')
    keyboard.add(key_path1)
    key_path2 = types.InlineKeyboardButton(text='Второй маршрут', callback_data='two')
    keyboard.add(key_path2)
    key_path3 = types.InlineKeyboardButton(text='Третий маршрут', callback_data='three')
    keyboard.add(key_path3)
    key_path4 = types.InlineKeyboardButton(text='Создать самому', callback_data='my_path')
    keyboard.add(key_path4)
    question = 'Выберите, пожлауйста, маршрут или создайте сами'
    tb.reply_to(message, text=question, reply_markup=keyboard)


def step_path(message, place_info: tuple, song_info: tuple):
    tb.send_message(message.chat.id, f'Идите в {place_info[0]}')
    locathion = place_info[3].split(",")
    tb.send_location(message.chat.id, locathion[0], locathion[1])
    tb.send_message(message.chat.id, f'Этот трек поможет скоротать время в пути до {place_info[0]}')
    media_from_bot.media(message.chat.id, song_info[1])
    tb.send_message(message.chat.id, 'Напишите: Пришел, когда дойдете до места\n'
                                     'Напишите: Стоп, чтобы закончить эксаурсию')


def step_info(message, place_info: tuple):
    tb.send_message(message.chat.id,
                    'Добро пожаловать на внеочередную остановку!\n'
                    'Ниже вы увидете всю информацию по этому месту в рамках нашей экскурсии')
    media_from_bot.media(message.chat.id, place_info[1])
    media_from_bot.audio(message.chat.id, place_info[2])
    tb.send_message(message.chat.id, 'Напишите: Далее для продолжения\n'
                                     'Напишите: Стоп, чтобы закончить эксаурсию')