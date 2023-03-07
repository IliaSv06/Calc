import sqlite3 as sql
from datetime import date
import time

def CreateDB():
    """Создаёт БД, вызвать при запуске приложения"""
    with sql.connect('History.db') as con:
        cur = con.cursor()

        cur.execute("""
                CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                decision TEXT NOT NULL,
                answer TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL)
        """)

def InsertData(decision, answer):
    """Заполняет БД. Принимает: решение и ответ"""
    try:
        with sql.connect('History.db') as con:
            cur = con.cursor()
            cur.execute(f"""
            INSERT INTO history (decision, answer, date, time)
            VALUES ('{str(decision)}', '{str(answer)}', '{str(date.today())}', '{str(time.strftime('%H.%M.%S'))}')
            """)
    except:
        print('Ошибка в добавлении данных')


def SelectData():
    """Возвращает список из картеджей вида:(решение, ответ, дата операции, время операции)"""
    with sql.connect('History.db') as con:
        cur = con.cursor()
        cur.execute("""
        SELECT decision, answer, date, time FROM history""")
        return [' '.join(x for x in i) for i in cur.fetchall()]

def clear_data():
    """Очищает историю"""
    with sql.connect('History.db') as con:
        cur = con.cursor()
        cur.execute("""
        DELETE FROM history""")
