import xml.etree.ElementTree as ET
import sqlite3

conn=sqlite3.connect('trka.sqlite')
cur=conn.cursor()

cur.executescript('''
            CREATE TABLE IF NOT EXISTS Artist(
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Track(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
)
''')

def lookup(d,key):
    found=False
    for i in d:
        if found:return i.text
        if i.tag=='key' and i.text==key:
            found=True
    return None

s=input('Enter file name: ')
xm=ET.parse(s)

l=xm.findall('dict/dict/dict')

for i in l:
    if lookup(i,'Track ID') is None: continue

    name=lookup(i,'Name')
    artist=lookup(i,'Artist')
    album=lookup(i,'Album')
    genre=lookup(i,'Genre')
    count=lookup(i,'Play Count')
    rating=lookup(i,'Rating')
    length=lookup(i,'Total Time')

    if name is None or artist is None or album is None or genre is None:continue

    cur.execute('INSERT OR IGNORE INTO Artist(name) VALUES (?)',(artist,))
    cur.execute('SELECT id FROM Artist WHERE name=?',(artist,))
    artist_id=cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Album(title,artist_id) VALUES (?,?)',(album,artist_id))
    cur.execute('SELECT id FROM Album WHERE title=?',(album,))
    album_id=cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Genre(name) VALUES (?)',(genre,))
    cur.execute('SELECT id FROM Genre WHERE name=?',(genre,))
    genre_id=cur.fetchone()[0]

    cur.execute('INSERT OR REPLACE INTO Track(title,album_id,genre_id,len,rating,count) VALUES (?,?,?,?,?,?)',(name,album_id,genre_id,length,rating,count))
conn.commit()
