# -*- coding: utf-8 -*-

import os
import time
from selenium import webdriver

driver_options = webdriver.firefox.options.Options()
driver_options.add_argument('--headless')
# Disabling webdriver`s cache:
ff_profile = webdriver.FirefoxProfile()
ff_profile.set_preference('javascript.enabled', False)
ff_profile.set_preference("browser.cache.disk.enable", False)
ff_profile.set_preference("browser.cache.memory.enable", False)
ff_profile.set_preference("browser.cache.offline.enable", False)
ff_profile.set_preference("network.http.use-cache", False)
ff_profile.set_preference('dom.caches.enabled', False)
ff_profile.set_preference('dom.prototype_document_cache.enabled', False)
ff_profile.set_preference('extensions.getAddons.cache.enabled', False)


driver = webdriver.Firefox(executable_path = 'geckodriver.exe', 
                           options = driver_options)

directory = 'thriller'
films = os.listdir('{0}/films'.format(directory))

for film_number, film in enumerate(films):
    
    film_file = open('{0}/films/{1}'.format(directory, film), 'r')
    film_string = film_file.read()
    film_link = film_string.split('|')[4]
    film_name = film_string.split('|')[0]
    film_rating = film_string.split('|')[1]
    film_country = film_string.split('|')[2]
    film_genre = film_string.split('|')[3]
    
    if ((film_number + 1)% 50 == 0):
        # Restarting webdriver to increase efficiency
        print('Restarting webdriver...')
        driver.quit()
        driver = webdriver.Firefox(executable_path = 'geckodriver.exe', 
                           options = driver_options)
        driver.get(film_link)
    else:
        driver.get(film_link)
        
    if (film_number == 0):
        driver.maximize_window()
    #div.styles_rowLight__3uy9z:nth-child(5)
    #div.styles_rowDark__2qC4I:nth-child(5)
    try:
        film_director = driver.find_element_by_css_selector('div.styles_rowDark__2qC4I:nth-child(5)').text.split('\n')[1]
    except:
        film_director = driver.find_element_by_css_selector('div.styles_rowLight__3uy9z:nth-child(5)').text.split('\n')[1]
    print('Film {0}: director {1}'.format(film_number + 1, film_director))
    
    film_synopsis = driver.find_element_by_class_name('styles_filmSynopsis__zLClu').text
    film_file.close()
    
    film_file = open('{0}/films/{1}'.format(directory, film), 'w')
    write_string = '{0}|{1}|{2}|{3}|{4}|{5}|{6}'.format(film_name, 
                                                        film_rating, 
                                                        film_country, 
                                                        film_genre, 
                                                        film_link,
                                                        film_director,
                                                        film_synopsis)
    try:
        film_file.write(write_string)
    except:
        print('Write error occured at film {0}'.format(film_name))
        continue
    film_file.close()
    if (film_number == len(films) - 1):
        driver.quit()
