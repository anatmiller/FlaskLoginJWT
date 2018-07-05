import sqlite3  # Import the SQLite3 module
import sys


def create_db():
    try:
        db = sqlite3.connect('data/mydb.db')
        cursor = db.cursor()
        cursor.execute('''DROP TABLE IF EXISTS sessions''')
        cursor.execute('''DROP TABLE IF EXISTS users''')
        cursor.execute("""
                          CREATE TABLE IF NOT EXISTS users(
                                                          id INTEGER PRIMARY KEY, 
                                                          email TEXT UNIQUE, 
                                                          password CHAR(64))
                        """)
        cursor.execute("""
                          CREATE TABLE IF NOT EXISTS sessions(
                                                            key TEXT UNIQUE PRIMARY KEY,
                                                            expires TIMESTAMP
                                                            )
                       """)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def create_or_update_session(key, expires):
    try:
        db = sqlite3.connect('../data/mydb.db')
        cur = db.cursor()
        cur.execute("INSERT OR REPLACE  INTO sessions VALUES (?,?)", (key, expires))
        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


def get_active_users():
    from datetime import datetime, timedelta
    try:
        db = sqlite3.connect('../data/mydb.db')
        cur = db.cursor()
        cur.execute("SELECT key FROM sessions WHERE expires >= ?",
                    (datetime.now(),))

        active_users = cur.fetchall()
        return [i[0] for i in active_users]

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def seed_db():
    from config import users
    try:
        db = sqlite3.connect('data/mydb.db')
        cursor = db.cursor()
        cursor.executemany(''' INSERT INTO users(email, password) VALUES(?,?)''', users)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def select_all(table_name):
    try:
        db = sqlite3.connect('data/mydb.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM " + table_name)
        all_rows = cursor.fetchall()
        for row in all_rows:
            for col in row:
                print(str(col) + ' ', end='')
            print('')
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_user(email):
    try:
        db = sqlite3.connect('../data/mydb.db')
        cursor = db.cursor()
        cursor.execute('''SELECT email,password FROM users WHERE email=?''', (email,))
        user_record = cursor.fetchone()
        return user_record

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == '__main__':
    if any("create" in s for s in sys.argv):
        create_db()

    if any("seed" in s for s in sys.argv):
        seed_db()

    if any("select-users" in s for s in sys.argv):
        select_all('users')

    if any("select-sessions" in s for s in sys.argv):
        select_all('sessions')
