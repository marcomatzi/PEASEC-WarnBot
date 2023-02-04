import os
import sys
import sqlite3


class Database:

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
              "warntype INTEGER, " \
              "severity REAL, " \
              "type TEXT," \
              "geo TEXT," \
              "source TEXT)"
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
        #print(db + ": " + sql)
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
    def get_query(table_name):
        print("Print Tabelle: ", table_name)
        conn = sqlite3.connect("warn.db")
        c = conn.cursor()

        query = "SELECT * FROM {}".format(table_name)
        c.execute(query)

        rows = c.fetchall()
        for row in rows:
            print(row)

        conn.close()

    def check_if_exist(self, tbl_name, db, where, where_val):
        conn = sqlite3.connect(db)
        c = conn.cursor()

        # Check if the entry already exists
        if isinstance(where_val, str):
            c.execute("SELECT * FROM {} WHERE {}='{}'".format(tbl_name, where, where_val))
        else:
            c.execute("SELECT * FROM ? WHERE ?=?", (tbl_name, where, where_val))

        result = c.fetchone()
        conn.close()
        return result