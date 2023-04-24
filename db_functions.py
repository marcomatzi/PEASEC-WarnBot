import configparser
import os
import sys
import sqlite3
from datetime import datetime



class Database:
    """def __init__(self, dbname):
        self.name = dbname"""

    @staticmethod
    def create_db():
        """
            Erstellt eine DB mit den Tabellen
        """

        config = configparser.ConfigParser()
        config.read("config.ini")
        config_db = config["Datenbank"]
        # Existenz feststellen
        if os.path.exists(config_db['PATH']):
            print("Datei bereits vorhanden")
            raise Exception("This is an exception")

        # Verbindung zur Datenbank erzeugen
        connection = sqlite3.connect(config_db['PATH'])

        # Datensatz-Cursor erzeugen
        cursor = connection.cursor()

        # Datenbanktabelle erzeugen
        sql = "CREATE TABLE notfalltipps (id INTEGER PRIMARY KEY, kategorie TEXT, kategorie2 TEXT, titel TEXT,  inhalt TEXT)"
        cursor.execute(sql)

        sql = 'CREATE TABLE "user_groups" ("ID" INTEGER, "group_nr" INTEGER, "description" TEXT, PRIMARY KEY("ID" AUTOINCREMENT))'
        cursor.execute(sql)

        sql = 'CREATE TABLE "users" ("id" INTEGER, "uid" NUMERIC, "name" TEXT, "lang" TEXT, "warnings" TEXT, "chatid" INTEGER, "group_id" INTEGER, "pref_location" TEXT, PRIMARY KEY("id" AUTOINCREMENT))'
        cursor.execute(sql)

        sql = 'CREATE TABLE "warning_information" ("id" INTEGER, "wid" TEXT, "version" INTEGER, "sender" TEXT, "status" TEXT, "msgType" TEXT, "scope" TEXT, "senderName" TEXT, "headline" TEXT, "text" TEXT, "web" TEXT, "areaDesc" TEXT, "codeIMG" TEXT, "image" TEXT, "event" TEXT, "urgency" TEXT, "severity" TEXT, "certainty" TEXT, "DateEffective" TEXT, "DateOnset" TEXT, "DateExpires" TEXT, "instruction" TEXT, PRIMARY KEY("id" AUTOINCREMENT))'
        cursor.execute(sql)

        sql = 'CREATE TABLE "warnings" ("id" INTEGER, "wid" TEXT, "title_de" TEXT, "title_en" TEXT, "version" INTEGER, "severity" REAL, "type" TEXT, "geo" TEXT, "source" TEXT, "descr" TEXT, "last_update" TEXT, "image" TEXT, PRIMARY KEY("id" AUTOINCREMENT))'
        cursor.execute(sql)

        sql = 'CREATE TABLE warntype(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,type TEXT)'
        cursor.execute(sql)

        connection.close()

    @staticmethod
    def execute_db(sql, db):
        """
        Führt ein query in der DB aus
        :param sql:
        :param db:
        :return:
        """
        # Verbindung zur Datenbank erzeugen
        connection = sqlite3.connect(db)
        # Datensatz-Cursor erzeugen
        cursor = connection.cursor()
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%S")
        # print("[db_insert][" + current_time + "]" + db + ": " + sql)

        cursor.execute(sql)
        connection.commit()
        connection.close()
        return True

    @staticmethod
    def insert_multiple(sql, db):
        """
        Fügt mehrere Parameter in warntype hinzu
        :param sql:
        :param db:
        :return:
        """
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        # print(db + ": " + sql)
        cursor.executemany("insert into warntype (name, type) values (?, ?)", sql)
        connection.commit()
        connection.close()

    @staticmethod
    def delete_query(sql, db):
        """
        Löscht ein eintrag aus der DB
        :param sql:
        :param db:
        :return:
        """
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        # print(db + ": " + sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()

    @staticmethod
    def get_query(table_name, where=None):
        """
        Gibt das result einer QUERY aus der DB zurück.
        Where ist hierbei optional.
        :param table_name:
        :param where:
        :return:
        """
        config = configparser.ConfigParser()
        config.read("config.ini")
        config_db = config["Datenbank"]

        # print("Print Tabelle: ", table_name)
        conn = sqlite3.connect(config_db['PATH'])
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
        """
        Gibt das Result einer Abfrage zurück. Diese Funktion ist Variable durch die Tabelle, DB, Where und Value für Where
        :param tbl_name:
        :param db:
        :param where:
        :param where_val:
        :return:
        """
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
        """
        Gibt alle user aus
        :param where:
        :return:
        """
        userlist = self.get_query("users", where)
        liste = []
        for e in userlist:
            tmp = [e[2], e[5]]  # Zwischenspeichern von name und chat_id
            liste.append(tmp)  # In eine neue Liste einfügen, die nur name und chat_id beinhaltet

        # print(liste)
        return userlist

    @staticmethod
    def count_rows(table, where=None):
        """
        Zählt die Anzahl von Einträgen anhand von Tabelle und Where
        :param table:
        :param where:
        :return:
        """
        arr = Database.get_query(table, where)
        # print("coming %", len(arr))
        return len(arr)


"""db = Database()
db.send_all_users_msg("test", "name like 'marco'")"""
