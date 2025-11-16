import sqlite3

con = sqlite3.connect('main.db')
cur = con.cursor()

SORTED_TYPE = ['Aa', 'El']
FILTER_TYPE = [i[0] for i in cur.execute('SELECT title FROM types')]
GENRES = [i[0] for i in cur.execute('SELECT title FROM genres')]

cur.close()