import os

directory = 'thriller'

films = os.listdir('{0}/films'.format(directory))
counter_films = 0
counter_posters = 0
for film in films:
    if (os.path.getsize('{0}/films/{1}'.format(directory, film)) == 0):
        os.remove('{0}/films/{1}'.format(directory, film))
        counter_films += 1
posters = os.listdir('{0}/posters'.format(directory))
for poster in posters:
    if (os.path.getsize('{0}/posters/{1}'.format(directory, poster)) == 0):
        os.remove('{0}/posters/{1}'.format(directory, poster))
        counter_posters += 1
        
print('Deleted {0} films, {1} posters'.format(counter_films, counter_posters))