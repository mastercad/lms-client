import sqlite3
import os.path

class Db(object):

    def __init__(self, db_name):
        self.db_name = db_name

        if not os.path.isfile(self.db_name):
            init_db()
        else:
            self.conn = sqlite3.connect(self.db_name)

    def init_db(self, cursor):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor.execute('''CREATE TABLE mappings (data text, trans text, symbol text, gty real, price real)''')
        self.cursor.execute("INSERT INTO stocks VALUES ('2006-01-05', 'BUY', 'RHAT', 100, 35.14)")
        self.cursor.commit()

    def __del__(self):
        self.conn.close()

try:
    db = Db("test.db")
    cursor = db.conn.cursor();
    print(cursor.execute("SELECT * FROM stocks"))

except Exception as exception:
    print("ERROR: "+str(exception))
