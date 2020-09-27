# -*- coding: utf-8 -*-

import requests
import telebot
import time
import datetime
import random
import os

categories = ['sci-fi',
              'comedy',
              'thriller',
              'fantasy',
              'crime',
              'best250']

token = '*********'
kinobot = telebot.TeleBot(token)

@kinobot.message_handler(content_types = ['text'])
def msg_handle(message):
    chat_id = message.chat.id
    curr_time = datetime.datetime.now()
    print('<{0}:{1}:{2}> Got command: {3}'.format(curr_time.hour, curr_time.minute, curr_time.second, message.text))
    def combine_film(category):
        films = os.listdir(category + '/films')
        filmnum = random.randint(0, len(films) - 1)
        film = films[filmnum]
        film_file = open(category + '/films/' + film, 'r')
        output_string = ''
        film_properties = film_file.read().split('|')
        output_string += '<b>'+film_properties[0]+'<b>' + '\n\n'
        output_string += film_properties[3].capitalize() + '\n'
        output_string += film_properties[2] + '\n'
        output_string += 'Оценка на кинопоиске: ' + film_properties[1] + '\n'
        output_string += 'Режиссер: ' + film_properties[5] + '\n\n'
        output_string += film_properties[6] + '\n\n'
        return [film[0:len(film) - 4], output_string]
        
    if (message.text == '/start'):
        kinobot.send_message(chat_id, 'Привет, я Кинобот. Я помогу подобрать фильм или сериал.')
        kinobot.send_message(chat_id, 'У меня есть несколько категорий фильмов. Пока их немного, '+
                     'но в дальнейшем мы расширим каталог. Вот команды для подбора фильмов'+
                     ' по разным категориям:\n\n')
        kinobot.send_message(chat_id, '"/250 Лучших" - один из 250 лучших фильмов по версии IMDb\n'+
                             '"/Триллер"\n' + 
                             '"/Комедия"\n' + 
                             '"/Фэнтези"\n' + 
                             '"/Научная фантастика"\n' + 
                             '"/Криминал"\n' + 
                             '"/Случайная категория"')
    elif (message.text == '/Случайная категория'):
        catnum = random.randint(0, len(categories) - 1)
        category = categories[catnum]
        processed_film = combine_film(category)
        film_poster = open(category + '/posters/' + processed_film[0] + '.jpg', 'rb')
        kinobot.send_message(chat_id, processed_film[1])
        kinobot.send_photo(chat_id, film_poster)
    elif (message.text == '/Триллер'):
        processed_film = combine_film('thriller')
        film_poster = open('thriller' + '/posters/' + processed_film[0] + '.jpg', 'rb')
        kinobot.send_message(chat_id, processed_film[1])
        kinobot.send_photo(chat_id, film_poster)
    elif (message.text == '/Комедия'):
        processed_film = combine_film('comedy')
        film_poster = open('comedy' + '/posters/' + processed_film[0] + '.jpg', 'rb')
        kinobot.send_message(chat_id, processed_film[1])
        kinobot.send_photo(chat_id, film_poster)
    elif (message.text == '/Фэнтези'):
        processed_film = combine_film('fantasy')
        film_poster = open('fantasy' + '/posters/' + processed_film[0] + '.jpg', 'rb')
        kinobot.send_message(chat_id, processed_film[1])
        kinobot.send_photo(chat_id, film_poster)
    elif (message.text == '/Криминал'):
        processed_film = combine_film('crime')
        film_poster = open('crime' + '/posters/' + processed_film[0] + '.jpg', 'rb')
        kinobot.send_message(chat_id, processed_film[1])
        kinobot.send_photo(chat_id, film_poster)
    elif (message.text == '/250 Лучших'):
        processed_film = combine_film('best250')
        film_poster = open('best250' + '/posters/' + processed_film[0] + '.jpg', 'rb')
        kinobot.send_message(chat_id, processed_film[1])
        kinobot.send_photo(chat_id, film_poster)
    elif (message.text == '/Научная фантастика'):
        processed_film = combine_film('sci-fi')
        film_poster = open('sci-fi' + '/posters/' + processed_film[0] + '.jpg', 'rb')
        kinobot.send_message(chat_id, processed_film[1])
        kinobot.send_photo(chat_id, film_poster)
    else:
        kinobot.send_message(chat_id, 'Извините, я вас не понимаю')

start_time = datetime.datetime.now()
print('<{0}:{1}:{2}> Starting...'.format(start_time.hour, start_time.minute, start_time.second))

if __name__ == '__main__':
    kinobot.polling()
end_time = datetime.datetime.now()
print('<{0}:{1}:{2}> Shutting down...'.format(end_time.hour, end_time.minute, end_time.second))
