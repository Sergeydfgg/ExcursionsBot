import telebot
import os
import bot_database

TOKEN = os.getenv("TG_TOKEN")
tb = telebot.TeleBot(TOKEN)


def message_parsing(message) -> tuple or str:
    try:
        u_log, fm, lm, gn = message.text.split()
        try:
            login_check = bot_database.read_from_db(u_log)
            if login_check is None:
                user = (u_log, fm, lm, gn, message.chat.id)
                return user
            elif login_check[0] == u_log:
                tb.send_message(message.chat.id, 'Такой логин уже есть')
                return 'login_is_busy'
            else:
                user = (u_log, fm, lm, gn, message.chat.id)
                return user
        except ValueError:
            user = (u_log, fm, lm, gn, message.chat.id) 
            return user
    except ValueError:
        tb.send_message(message.chat.id, 'Неверный формат ввода')


def place_preparathion(message) -> tuple:
    try:
        p_name, p_media, p_audio, p_point = message.text.split(";")
        place = (p_name, p_media, p_audio, p_point)
        return place
    except ValueError:
        tb.send_message(message.chat.id, 'Неверный формат ввода')


def song_preparathion(message) -> tuple:
    try:
        s_name, s_path = message.text.split(";")
        place = (s_name, s_path)
        return place
    except ValueError:
        tb.send_message(message.chat.id, 'Неверный формат ввода')
