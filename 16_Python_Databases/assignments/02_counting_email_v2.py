import sqlite3

url = input('Enter file name: ')
if len(url) < 1:
    url = 'mbox.txt'

try:
    file_handle = open(url)
except:
    print("Not found")
    exit()


def email_counter(file):
    counts = dict()
    for line in file:
        if not line.startswith('From: '):
            continue
        words = line.split()
        email = words[1]
        org = email.split('@')[1]
        counts[org] = counts.get(org, 0) + 1
    return counts


# ----------------------------------------------
# lst = re.findall('\\S+@\\S+', s)  # <=====
# ----------------------------------------------

conn = sqlite3.connect('emails_v2.sqlite')
cursor = conn.cursor()

cursor.execute('''DROP TABLE IF EXISTS Counts''')
cursor.execute('''CREATE TABLE Counts (org TEXT, count INTEGER)''')

counts_dict = email_counter(file_handle)
print(counts_dict)

for key, value in counts_dict.items():
    cursor.execute('INSERT INTO Counts (org, count) VALUES (?, ?)', (key, value))

conn.commit()

sql = 'SELECT org, count FROM Counts ORDER BY count DESC'
for row in cursor.execute(sql):
    print(str(row[0]), row[1])

cursor.close()
