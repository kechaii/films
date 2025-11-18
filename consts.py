import sqlite3

con = sqlite3.connect('main.db')
cur = con.cursor()

SORTED_TYPE = ['Алфавит', 'Рейтинг']
FILTER_TYPE = [i[0] for i in cur.execute('SELECT id FROM types')]
GENRES = [i[0] for i in cur.execute('SELECT id FROM genres')]

DICT_FILTER = {i[0] : en + 1 for en, i in enumerate(cur.execute('SELECT title FROM types'))}
DICT_GENRES = {i[0] : en + 1 for en, i in enumerate(cur.execute('SELECT title FROM genres'))}

DICT_FILTER_NUM = {en + 1 : i[0] for en, i in enumerate(cur.execute('SELECT title FROM types'))}
DICT_GENRES_NUM = {en + 1: i[0] for en, i in enumerate(cur.execute('SELECT title FROM genres'))}

cur.close()