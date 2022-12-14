import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cursor = conn.cursor()

cursor.execute('''DROP TABLE IF EXISTS Counts''')
cursor.execute('''CREATE TABLE Counts (email TEXT, count INTEGER)''')

filename = input('Enter file name: ')
if len(filename) < 1:
    filename = 'mbox-short.txt'

file_handle = open(filename)
for line in file_handle:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    email = pieces[1]

    cursor.execute('SELECT count FROM Counts WHERE email = ? ', (email,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute('INSERT INTO Counts (email, count) VALUES (?, 1)', (email,))
    else:
        cursor.execute('UPDATE Counts SET count = count + 1 WHERE email = ?',
                       (email,))
    conn.commit()

# https://www.sqlite.org/lang_select.html
sql_str = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cursor.execute(sql_str):
    print(str(row[0]), row[1])

cursor.close()
