import sqlite3



def createTable():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users2(username text, password text, canGenerateSentence boolean DEFAULT False)')
    conn.commit()
    conn.close()


def createUser(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO users2 VALUES(?,?,?)', (username, password, False))
    conn.commit()
    conn.close()

def giveAccess(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE users2 SET canGenerateSentence = ? WHERE username = ?', (True, username))
    conn.commit()
    conn.close()


def userExists(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT username FROM users2 WHERE username = ?', (username,))
    return c.fetchone()


def userHasAccess(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT canGenerateSentence FROM users2 WHERE username = ?', (username,))
    return c.fetchone()


def matching(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users2 WHERE username = ?', (username,))
    return c.fetchone() == password

def displayAllData():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users2')
    print(f"database contents: ")
    print(f"----"*20)
    for row in c.fetchall():
        print(f'\033[93m{row[0]}\033[0m \033[94m{row[1]}\033[0m \033[92m{row[2]}\033[0m')



createTable()
displayAllData()