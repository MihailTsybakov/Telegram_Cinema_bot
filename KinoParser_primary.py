# -*- coding: utf-8 -*-
import requests
import time
import datetime
import bs4
import selenium
import winsound
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

webdriver_options = Options()
webdriver_options.add_argument('--headless')
driver = webdriver.Firefox(executable_path = 'geckodriver.exe', options = webdriver_options)
print('Initialized webdriver...')

url = 'https://www.kinopoisk.ru/lists/navigator/Thriller/'
query_header = {'Accept' : 'text/html', 'User_Agent' : 'Mozilla/5.0 (Linux; '+
                'Android 5.0; SM-G920A) AppleWebKit (KHTML, like Gecko) Chrom'+
                'e Mobile Safari (compatible; AdsBot-Google-Mobile; +http://ww'+
                'w.google.com/mobile/adsbot.html)'}

directory = 'thriller'

stop_value = 6
iteration_index = 0
while True:
    if (stop_value != 0):
        if(iteration_index > stop_value - 1):
            break
    
    driver.get(url + '?page={0}&quick_filters=available_online&tab=online'.format(iteration_index + 1))
    if (iteration_index == 0):
        time.sleep(15)
    driver.maximize_window()
    
    film_names = driver.find_elements_by_class_name('selection-film-item-meta__name')
    film_ratings = driver.find_elements_by_class_name('rating.film-item-user-data__rating')
    film_infos = driver.find_elements_by_class_name('selection-film-item-meta__met'+
                                                  'a-additional-item')
    film_posters = driver.find_elements_by_class_name('selection-film-item-poster'+
                                                    '__image')
    film_links = driver.find_elements_by_class_name('selection-film-item-meta__link')
    print('{0} {1} {2} {3} {4}'.format(len(film_names),
                                       len(film_ratings),
                                       len(film_infos),
                                       len(film_posters),
                                       len(film_links)))
    for index in range(0, len(film_names)):
        film_names[index] = film_names[index].text
        film_ratings[index] = film_ratings[index].text.split('\n')[0]
        film_infos[2*index] = film_infos[2*index].text
        film_infos[2*index + 1] = film_infos[2*index + 1].text
        film_posters[index] = film_posters[index].get_attribute('src')
        film_links[index] = film_links[index].get_attribute('href')
        
    for index in range(0, len(film_names)):
        try:
            film_file = open('{0}/films/{1}.txt'.format(directory,film_names[index]), 'w')
        except:
            continue
        write_string = '{0}|{1}|{2}|{3}|{4}|'.format(film_names[index], 
                                            film_ratings[index], 
                                            film_infos[2*index], 
                                            film_infos[2*index + 1],
                                            film_links[index])
        film_file.write(write_string + '\n')
        film_file.close()
        
        film_poster = requests.get(film_posters[index], headers = query_header)
        poster_image = open('{0}/posters/{1}.jpg'.format(directory,film_names[index]), 
                            'wb')
        poster_image.write(film_poster.content)
        poster_image.close()
        
    try:
        changepage_btns = webdriver.find_elements_by_class_name('paginator__page-relative')
        btns_text = []
        for btn in changepage_btns:
            btns_text.append(btn.text)
        if (btns_text.count('Вперёд') != 1):
            break
        for btn in changepage_btns:
            if (btn.text == 'Вперёд'):
                btn.click()
    except:
        pass
        
    iteration_index += 1
    print('Processed page {0}'.format(iteration_index))
    winsound.Beep(1200, 400)
    
driver.quit()