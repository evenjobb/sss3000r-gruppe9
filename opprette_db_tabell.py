import sqlite3 as lite
import sys

def opprett():
    connection = lite.connect('bilder.db')
    with connection:
        cur = connection.cursor()
        cur.execute('DROP TABLE IF EXISTS bilder')
        cur.execute('CREATE TABLE bilder(id INTEGER PRIMARY KEY, path varchar(255), tidspunkt DATETIME, dato TEXT)')
