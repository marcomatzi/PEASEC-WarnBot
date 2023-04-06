import os
import sys
import sqlite3
from datetime import datetime



class Database:
    """def __init__(self, dbname):
        self.name = dbname"""

    @staticmethod
    def create_db():
        # Existenz feststellen
        if os.path.exists("warn.db"):
            print("Datei bereits vorhanden")
            raise Exception("This is an exception")

        # Verbindung zur Datenbank erzeugen
        connection = sqlite3.connect("warn.db")

        # Datensatz-Cursor erzeugen
        cursor = connection.cursor()

        # Datenbanktabelle erzeugen
        sql = "CREATE TABLE warnings(" \
              "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
              "wid TEXT, " \
              "title_de TEXT, " \
              "title_en TEXT, " \
              "version INTEGER, " \
              "severity TEXT, " \
              "type TEXT," \
              "geo TEXT," \
              "source TEXT," \
              "descr TEXT)"
        cursor.execute(sql)

        sql = "CREATE TABLE users(" \
              "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
              "uid NUMERIC, " \
              "name TEXT, " \
              "lang TEXT, " \
              "warnings INTEGER" \
              "chatid INTEGER)"
        cursor.execute(sql)

        sql = "CREATE TABLE warntype(" \
              "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
              "name TEXT," \
              "type TEXT)"
        cursor.execute(sql)
        connection.close()

    @staticmethod
    def execute_db(sql, db):
        # Verbindung zur Datenbank erzeugen
        connection = sqlite3.connect(db)
        # Datensatz-Cursor erzeugen
        cursor = connection.cursor()
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%S")
        # print("[db_insert][" + current_time + "]" + db + ": " + sql)
        """        
        #### REPLACE
        # split the query by comma
        query_list = sql.split(',')

        # iterate over each column
        for i in range(len(query_list)):
            # check if the column has ' or "
            if "'" in query_list[i] or '"' in query_list[i]:
                # replace ' or " with -
                query_list[i] = query_list[i][1:-1].replace("'", "''")
                query_list[i] = query_list[i].replace("`", "''")
        """

        cursor.execute(sql)
        connection.commit()
        connection.close()
        return True

    @staticmethod
    def insert_multiple(sql, db):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        # print(db + ": " + sql)
        cursor.executemany("insert into warntype (name, type) values (?, ?)", sql)
        connection.commit()
        connection.close()

    @staticmethod
    def delete_query(sql, db):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        # print(db + ": " + sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()

    @staticmethod
    def get_query(table_name, where=None):
        # print("Print Tabelle: ", table_name)
        conn = sqlite3.connect("warn.db")
        c = conn.cursor()

        if where is None:
            query = "SELECT * FROM {}".format(table_name)
        else:
            query = "SELECT * FROM {} WHERE {}".format(table_name, where)
        c.execute(query)

        rows = c.fetchall()
        # print(rows)
        """for row in rows:
            print(row)"""
        conn.close()
        return rows

    @staticmethod
    def check_if_exist(tbl_name, db, where, where_val):
        conn = sqlite3.connect(db)
        c = conn.cursor()

        # Check if the entry already exists
        if isinstance(where_val, str):
            c.execute("SELECT * FROM {} WHERE {}='{}'".format(tbl_name, where, where_val))
        else:
            c.execute("SELECT * FROM {} WHERE {} = {}".format(tbl_name, where, where_val))

        result = c.fetchone()
        conn.close()
        return result

    def get_users(self, where=None):
        userlist = self.get_query("users", where)
        liste = []
        for e in userlist:
            tmp = [e[2], e[5]]  # Zwischenspeichern von name und chat_id
            liste.append(tmp)  # In eine neue Liste einfügen, die nur name und chat_id beinhaltet

        # print(liste)
        return userlist

    @staticmethod
    def count_rows(table, where=None):
        arr = Database.get_query(table, where)
        # print("coming %", len(arr))
        return len(arr)


"""db = Database()
db.send_all_users_msg("test", "name like 'marco'")"""
