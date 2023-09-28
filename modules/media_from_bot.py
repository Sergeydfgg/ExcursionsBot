import telebot
import os

TOKEN = os.getenv("TG_TOKEN")
tb = telebot.TeleBot(TOKEN)


def audio(c_id: int, path):
    audio = open(path, 'rb')
    tb.send_audio(c_id, audio)


def media(c_id: int, path):
    media = open(path, 'rb')
    tb.send_document(c_id, media)


def photoes(c_id: int, path):
    photo = open(path, 'rb')
    tb.send_photo(c_id, photo)
