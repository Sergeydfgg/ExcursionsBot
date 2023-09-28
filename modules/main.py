import sqlite3

import telebot
import os
from telebot import types
import bot_database
import excursion
import user_opinion_get
from random import randint

TOKEN = os.getenv("TG_TOKEN")
ussage = "Список команд:\n " \
         "Маршрут - все доустунпые маршруты\n " \
         "Привет - получить свое привествие\n" \
         "/reg - регистрация\n" \
         "/showme - информация о вашем профиле\n" \
         "/deleteme - удалить себя из базы данных\n" \
         "Описание маршрутов - получить дополнительную информацию про доступные маршруты" \
         " и конструктор маршрутов\n"


tb = telebot.TeleBot(TOKEN)


def say_hi(message):
    tb.reply_to(message, "Здарова, братулек")


def add_place_to_list(message, name_of_place: str, list_key: int):
    try:
        excursion.pathes_of_users.set_new_place(list_key,
                                                excursion.availabe_places[excursion.place_control_sum(name_of_place)])
        tb.send_message(message.chat.id,
                        'Введите навзвание песни, которую хотите послушать по пути до места')
        tb.register_next_step_handler(message, add_song_to_list, list_key)
    except KeyError:
        tb.send_message(message.chat.id, 'Такого места нет, проверьте корректность ввода')
        tb.register_next_step_handler(message, path_generathion, list_key)


def add_song_to_list(message, list_key: int):
    try:
        excursion.pathes_of_users.set_new_song(list_key,
                                               excursion.availabe_songs[excursion.place_control_sum(message.text)])
        tb.send_message(message.chat.id,
                        'Введите название следующего места или напишите Загрузить для формирования маршрута')
        tb.register_next_step_handler(message, path_generathion, list_key)
    except KeyError:
        tb.send_message(message.chat.id, 'Такой песни нет, проверьте корректность ввода')
        tb.register_next_step_handler(message, add_song_to_list, list_key)


def path_generathion(message, key_for_new_list: int):
    if message.text == 'Выберите, пожлауйста, маршрут или создайте сами':
        list_of_places = []
        list_of_songs = []
        excursion.pathes_of_users.add_new_list(key_for_new_list, list_of_places)
        excursion.pathes_of_users.add_new_song_list(key_for_new_list, list_of_songs)
        tb.register_next_step_handler(message, path_generathion, key_for_new_list)
    elif message.text != 'Выберите, пожлауйста, маршрут или создайте сами':
        if message.text == 'Загрузить':
            tb.send_message(message.chat.id, 'Все готово, напишите Далее для начала экскурсии')
            tb.register_next_step_handler(message, step_path_control, key_for_new_list, 0)
        elif message.text != 'Загрузить':
            add_place_to_list(message, message.text, key_for_new_list)


def step_path_control(message, key_of_path: int, current_step: int):
    if current_step < len(excursion.pathes_of_users.places_dict[key_of_path]):
        if message.text == 'Стоп':
            tb.send_message(message.chat.id, 'Конец экскурсии')
            excursion.pathes_of_users.delete_places_path(key_of_path)
            excursion.pathes_of_users.delete_song_list(key_of_path)
            return
        elif message.text == 'Далее':
            place_array = excursion.pathes_of_users.places_dict[key_of_path]
            song_array = excursion.pathes_of_users.song_dict[key_of_path]
            place_info = bot_database.read_from_db_places(place_array[current_step])
            song_info = bot_database.read_from_db_song(song_array[current_step])
            excursion.step_path(message, place_info, song_info)
            tb.register_next_step_handler(message, step_info_control, key_of_path, current_step)
        elif message.text != 'Далее':
            tb.send_message(message.chat.id, 'Неверная команда, введите Далее для продолжения')
            tb.register_next_step_handler(message, step_path_control, key_of_path, current_step)
    elif current_step >= len(excursion.pathes_of_users.places_dict[key_of_path]):
        tb.send_message(message.chat.id, 'Конец экскурсии')
        excursion.pathes_of_users.delete_places_path(key_of_path)
        excursion.pathes_of_users.delete_song_list(key_of_path)


def step_info_control(message, key_of_path: int, current_step: int):
    if current_step < len(excursion.pathes_of_users.places_dict[key_of_path]):
        if message.text == 'Стоп':
            tb.send_message(message.chat.id, 'Конец экскурсии')
            excursion.pathes_of_users.delete_places_path(key_of_path)
            excursion.pathes_of_users.delete_song_list(key_of_path)
            return
        if message.text == 'Пришел':
            place_array = excursion.pathes_of_users.places_dict[key_of_path]
            place_info = bot_database.read_from_db_places(place_array[current_step])
            excursion.step_info(message, place_info)
            current_step += 1
            tb.register_next_step_handler(message, step_path_control, key_of_path, current_step)
        elif message.text != 'Пришел':
            tb.send_message(message.chat.id, 'Неверная команда, введите Пришел для продолжения\n'
                                             'Введите Стоп, чтобы закончить экскурсию')
            tb.register_next_step_handler(message, step_info_control, key_of_path, current_step)
    elif current_step >= len(excursion.pathes_of_users.places_dict[key_of_path]):
        tb.send_message(message.chat.id, 'Конец экскурсии')
        excursion.pathes_of_users.delete_places_path(key_of_path)
        excursion.pathes_of_users.delete_song_list(key_of_path)


def user_opinion_control(message, op_step: int):
    if message.text == 'Отзыв':
        part_of_opinion = []
        user_name = bot_database.read_from_db_by_id(message.chat.id)
        tb.send_message(message.chat.id, 'Расскажите, что вам понравилось')
        tb.register_next_step_handler(message, user_opinion_get.add_pluses_part, part_of_opinion)
        tb.send_message(message.chat.id, 'Расскажите, что вам не понравилось')
        tb.register_next_step_handler(message, user_opinion_get.add_minuses_part, part_of_opinion)
        tb.send_message(message.chat.id, 'Поставьте оценку от 1 до 10')
        tb.register_next_step_handler(message, user_opinion_get.add_pluses_part, part_of_opinion)
    elif message.text == 'Пропустить':
        pass


@tb.message_handler(commands=['start'])
def command_start(message):
    tb.reply_to(message, 'Вас приветствует бот-эксукрсовод. На данный момент у нас есть для вас 3 маршрута, для выбора одного '
                         'из них введите команду: Маршрут. Для дполнительной информации введите: /help.')


@tb.message_handler(commands=['help'])
def command_help(message):
    tb.reply_to(message, ussage)


@tb.message_handler(content_types=['text'])
def check(message):
    if message.text == 'Привет':
        say_hi(message)
    elif message.text == 'Маршрут':
        excursion.path_choice(message)
    elif message.text == 'Скинь клавиатуру':
        tb.send_message(message.chat.id, 'А ебало тебе не скинуть?')
    elif message.text == '/reg':
        tb.send_message(message.from_user.id, 'Для регистрации придумайте себе логин,'
                                              ' а также укажите основную информацию о '
                                              'себе в формате: Логин Имя Фамилия Гендер')
        tb.register_next_step_handler(message, bot_database.prepare_message_to_write)
    elif message.text == 'DeleteAllUsers':
        try:
            bot_database.clear_db()
            tb.send_message(message.chat.id, 'Таблица очищена')
        except sqlite3.Error:
            tb.send_message(message.chat.id, 'Непредвиденная ошибка')
    elif message.text == '/showme':
        tb.send_message(message.chat.id, 'Введи свой логин')
        tb.register_next_step_handler(message, bot_database.id_check)
    elif message.text == 'DB_recreate':
        bot_database.db_recreathion()
        tb.send_message(message.from_user.id, 'Базы данных созданы')
    elif message.text == 'Add_new_place':
        tb.send_message(message.chat.id, 'Введите Название места;Путь до медиа файла;'
                                         'Путь до аудио файла;Путь до точки в таком формате')
        tb.register_next_step_handler(message, bot_database.prepare_place_to_write)
    elif message.text == 'Add_new_song':
        tb.send_message(message.chat.id, 'Введите Название песни;Путь до песни в таком формате')
        tb.register_next_step_handler(message, bot_database.prepare_song_to_write)
    elif message.text == 'Check_place':
        tb.send_message(message.from_user.id, 'Введите название места для проверки')
        tb.register_next_step_handler(message, bot_database.place_check)
    elif message.text == 'Check_song':
        tb.send_message(message.from_user.id, 'Введите название песни для проверки')
        tb.register_next_step_handler(message, bot_database.song_check)
    elif message.text == 'DeleteAllPlaces':
        try:
            bot_database.clear_db_places()
            tb.send_message(message.chat.id, 'Таблица очищена')
        except sqlite3.Error:
            tb.send_message(message.chat.id, 'Непредвиденная ошибка')
    elif message.text == 'DeleteAllSongs':
        try:
            bot_database.clear_db_songs()
            tb.send_message(message.chat.id, 'Таблица очищена')
        except sqlite3.Error:
            tb.send_message(message.chat.id, 'Непредвиденная ошибка')
    elif message.text == '/deleteme':
        tb.send_message(message.chat.id, 'Введите свой логин')
        tb.register_next_step_handler(message, bot_database.delete_user_from_db)
    else:
        tb.send_message(message.chat.id, 'И как это понимать? Напиши /help для справки')


@tb.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "one":
        tb.send_message(call.message.chat.id, 'Вы выбрали первый маршрут')
        tb.send_message(call.message.chat.id, 'Мы пройдем по пути Второе место -> Первое место')
        list_of_places = ['Второе место', 'Первое место']
        list_of_songs = ['трах-трах', 'трах-трах']
        key = randint(1000, 2000)
        excursion.pathes_of_users.add_new_list(key, list_of_places)
        excursion.pathes_of_users.add_new_song_list(key, list_of_songs)
        tb.send_message(call.message.chat.id, 'Все готово, напишите Далее для начала экскурсии')
        tb.register_next_step_handler(call.message, step_path_control, key, 0)
    elif call.data == "two":
        tb.send_message(call.message.chat.id, 'Вы выбрали второй маршрут')
    elif call.data == "three":
        tb.send_message(call.message.chat.id, 'Вы выбрали третий маршрут')
    elif call.data == "my_path":
        tb.send_message(call.message.chat.id, 'Перед вами конструктор маршрута, введите название первого места')
        key = randint(1000, 2000)
        path_generathion(call.message, key)


tb.polling()
tb.polling(none_stop=True)
tb.polling(interval=2)

while True:
    pass
