import os
import sys
import sqlite3

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
        # Datensatz erzeugen
        """
        sql = "INSERT INTO warntype (name, type) VALUES('Katwarn', 'kat')"
        self.insert_into(sql, "warn.db")
        sql = "INSERT INTO warntype (name, type) VALUES('Biwapp', 'kat')"
        self.insert_into(sql, "warn.db")
        sql = "INSERT INTO warntype (name, type) VALUES('Mowas', 'kat')"
        self.insert_into(sql, "warn.db")
        sql = "INSERT INTO warntype (name, type) VALUES('DWD', 'Wetter')"
        self.insert_into(sql, "warn.db")
        sql = "INSERT INTO warntype (name, type) VALUES('Hochwasser Portal', 'kat')"
        self.insert_into(sql, "warn.db")
        sql = "INSERT INTO warntype (name, type) VALUES('Polizei', 'kat')"
        self.insert_into(sql, "warn.db")
        sql = "INSERT INTO warntype (name, type) VALUES('Covid', 'Covid')"
        self.insert_into(sql, "warn.db")
        """
        # Datensatz erzeugen
        # sql = "INSERT INTO personen VALUES('Schmitz', " \
        #       "'Peter', 81343, 3750, '12.04.1958')"
        # cursor.execute(sql)
        # connection.commit()

        # Datensatz erzeugen
        # sql = "INSERT INTO personen VALUES('Mertens', " \
        #      "'Julia', 2297, 3621.5, '30.12.1959')"
        # cursor.execute(sql)
        # connection.commit()

    @staticmethod
    def execute_db(sql, db):
        # Verbindung zur Datenbank erzeugen
        connection = sqlite3.connect(db)
        # Datensatz-Cursor erzeugen
        cursor = connection.cursor()
        print(db + ": " + sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()

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

    def get_query(self, table_name, where=None):
        print("Print Tabelle: ", table_name)
        conn = sqlite3.connect("warn.db")
        c = conn.cursor()

        if where is None:
            query = "SELECT * FROM {}".format(table_name)
        else:
            query = "SELECT * FROM {} WHERE {}".format(table_name, where)
        c.execute(query)

        rows = c.fetchall()
        #print(rows)
        """for row in rows:
            print(row)"""
        conn.close()
        return rows

    def check_if_exist(self, tbl_name, db, where, where_val):
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

    def send_all_users_msg(self, text, where=None):
        userlist = self.get_query("users", where)
        liste = []
        for e in userlist:
            tmp = [e[2], e[5]]  # Zwischenspeichern von name und chat_id
            liste.append(tmp)   # In eine neue Liste einfügen, die nur name und chat_id beinhaltet

        print(liste)
        return userlist


"""db = Database()
db.send_all_users_msg("test", "name like 'marco'")"""
