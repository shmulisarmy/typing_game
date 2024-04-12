import sqlite3



def createTable():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS accounts(username text, password text, canGenerateSentence boolean Default False)')
    conn.commit()
    conn.close()


def createUser(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO accounts VALUES(?,?)', (username, password))
    conn.commit()
    conn.close()

def giveAccess(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE accounts SET canGenerateSentence = ? WHERE username = ?', (True, username))
    conn.commit()
    conn.close()


def userHasAccess(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT canGenerateSentence FROM accounts WHERE username = ?', (username,))
    return c.fetchone()[0]


def matching(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT password FROM accounts WHERE username = ?', (username,))
    return c.fetchone()[0] == password




createTable()