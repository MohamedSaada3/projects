import json
import sqlite3

conn = sqlite3.connect('rosterdb-mine.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'course 4 assignments(databases)\\roster_data.json.json'  # Adjust the path accordingly

str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:
    name = entry[0]
    course = entry[1]
    role = entry[2]
    print((name, course, role))

    # Insert user
    cur.execute('''INSERT OR IGNORE INTO User (name) VALUES (?)''', (name,))
    cur.execute('SELECT id FROM User WHERE name = ?', (name,))
    user_id = cur.fetchone()[0]

    # Insert course
    cur.execute('''INSERT OR IGNORE INTO Course (title) VALUES (?)''', (course,))
    cur.execute('SELECT id FROM Course WHERE title = ?', (course,))
    course_id = cur.fetchone()[0]

    # Insert member
    cur.execute('''INSERT OR IGNORE INTO Member (user_id, course_id, role) VALUES (?, ?, ?)''', (user_id, course_id, role))

# Commit changes outside the loop
conn.commit()














# for role in json_data:
#     specific=json_data[index]
#     target=specific[2]
#     index=index+1
#     print(target)
#     print(type(role))
#     cur.execute('INSERT INTO Member (role) VALUES(?)',(role,))







    