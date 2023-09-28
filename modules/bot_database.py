import sqlite3
import os
import message_preparathion
import telebot

TOKEN = os.getenv("TG_TOKEN")
tb = telebot.TeleBot(TOKEN)


def db_recreathion():
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/usere.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
               userid TEXT,
               fname TEXT,
               lname TEXT,
               gender TEXT,
               user_chat_id INT);
            """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS users_opinion(
               UserId INTEGER PRIMARY KEY,
               ChatId INT,
               UserName TEXT,
               UserOpinionPluses TEXT,
               UserOpinionMinuses TEXT,
               UserRating INT);
            """)
    conn.commit()

    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/list_of_places.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS places(
               name_of_place TEXT,
               path_to_media TEXT,
               path_to_audio TEXT,
               path_to_point TEXT);
            """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS songs(
                   name_of_song TEXT,
                   path_to_song TEXT);
                """)
    conn.commit()


def read_from_db(user_log, message=None) -> tuple or str:
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/usere.db')
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE userid=(?);", (user_log,))
        one_result = cur.fetchone()
        if message is None:
            return one_result
        elif one_result[4] == message.chat.id or message.chat.id == os.getenv("ADMIN_CHAT_ID"):
            return one_result
        else:
            return 'bad_request'
    except ValueError:
        return 'bad_request'


def read_from_db_by_id(user_chat_id) -> tuple or str:
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/usere.db')
    cur = conn.cursor()
    try:
        cur.execute("SELECT userid FROM users WHERE user_chat_id=(?);", user_chat_id)
        one_result = cur.fetchone()
        return one_result
    except ValueError:
        return 'bad_request'


def read_from_db_places(name_of_place: str) -> tuple or str:
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/list_of_places.db')
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM places WHERE name_of_place=(?);", (name_of_place,))
        result = cur.fetchone()
        return result
    except ValueError:
        return 'bad_request'


def read_from_db_song(name_of_song: str) -> tuple or str:
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/list_of_places.db')
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM songs WHERE name_of_song=(?);", (name_of_song,))
        result = cur.fetchone()
        return result
    except ValueError:
        return 'bad_request'


def read_from_db_UserOp(user_name: str):
    pass


def prepare_message_to_write(message):
    user_buf = message_preparathion.message_parsing(message)
    if user_buf != 'login_is_busy':
        write_to_db(message, user_buf)


def prepare_place_to_write(message):
    place_buf = message_preparathion.place_preparathion(message)
    write_to_db_places(message, place_buf)


def prepare_song_to_write(message):
    song_buf = message_preparathion.song_preparathion(message)
    write_to_db_song(message, song_buf)


def write_to_db(message, user_data: tuple):
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/usere.db')
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", user_data)
        conn.commit()
        tb.send_message(message.from_user.id, 'Вы записаны в базу данных')
    except ValueError:
        tb.send_message(message.from_user.id, 'Ошибка записи в базу')


def write_to_db_places(message, place_data: tuple):
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/list_of_places.db')
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO places VALUES(?, ?, ?, ?);", place_data)
        conn.commit()
        tb.send_message(message.from_user.id, 'Место добавлено в базу')
    except ValueError:
        tb.send_message(message.from_user.id, 'Ошибка записи в базу')


def write_to_db_song(message, song_data: tuple):
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/list_of_places.db')
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO songs VALUES(?, ?);", song_data)
        conn.commit()
        tb.send_message(message.from_user.id, 'Песня добавлена в базу')
    except ValueError:
        tb.send_message(message.from_user.id, 'Ошибка записи в базу')


def write_to_db_UserOp(message, op_data: tuple):
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/usere.db')
    cur = conn.cursor()
    try:
        cur.execute("""INSERT INTO user_opinion(ChatId, UserName, UserOpinionPluses,
                       UserOpinionMinuses, UserRating) VALUES(?, ?, ?, ?, ?);""", op_data)
        conn.commit()
        tb.send_message(message.from_user.id, 'Отзыв добавлен')
    except ValueError:
        tb.send_message(message.from_user.id, 'Ошибка записи в базу')


def clear_db():
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/usere.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM users;")
    conn.commit()


def clear_db_places():
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/list_of_places.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM places;")
    conn.commit()


def clear_db_songs():
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/list_of_places.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM songs;")
    conn.commit()


def delete_user_from_db(message):
    conn = sqlite3.connect(r'C:/Users/Сергей/PycharmProjects/python_bot_project/database/usere.db')
    cur = conn.cursor()
    user_data = read_from_db(message.text)
    if user_data is None:
        tb.send_message(message.chat.id, 'Пользователь не найден')
    elif user_data[4] == message.chat.id:
        try:
            cur.execute("DELETE FROM users WHERE userid=(?);", (message.text,))
            conn.commit()
            tb.send_message(message.chat.id, 'Вы были удалены из базы данных')
        except TypeError:
            tb.send_message(message.chat.id, 'Пользователь не найден')

    else:
        tb.send_message(message.chat.id, 'Ошибка доступа')


def id_check(message):
    try:
        result = read_from_db(message.text, message)
        if result == 'bad_request':
            tb.send_message(message.chat.id, 'Неверный логин, bad request')
        else:
            tb.send_message(message.chat.id, f'Ваш логин: {result[0]}, Ваше имя: {result[1]}, '
                                             f'Ваша фамилия: {result[2]}, Вы по жизни: {result[3]}')
    except TypeError:
        tb.send_message(message.chat.id, 'Неверный логин')


def place_check(message):

    """    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    """

    try:
        result = read_from_db_places(message.text)
        if result == 'bad_request':
            tb.send_message(message.chat.id, 'Неверное место, bad request')
        else:
            tb.send_message(message.chat.id, f'Название места: {result[0]}, Путь до медиа файла: {result[1]}, '
                                             f'Путь до аудио файла: {result[2]}, Путь до точки маршрута: {result[3]}')
    except TypeError:
        tb.send_message(message.chat.id, 'Неверное место')


def song_check(message):
    try:
        result = read_from_db_song(message.text)
        if result == 'bad_request':
            tb.send_message(message.chat.id, 'Неверная песня, bad request')
        else:
            tb.send_message(message.chat.id, f'Название песни: {result[0]}, Путь до песни: {result[1]}')
    except TypeError:
        tb.send_message(message.chat.id, 'Неверное название')


def op_check(message):
    pass
