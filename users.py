"""
    Diese Klasse dient zur verwaltung für die Nutzer.
    Eintragen in die DB sowie versenden von Nachrichten
    -> Dauerhafte Ausführung der Module im Loop
"""
import configparser

import db_functions
from db_functions import Database
import logging


class Users:
    def __init__(self, userdata):
        self.uid = userdata
        self.logger = logging.getLogger(__name__)
        self.db = Database()
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.config_db = config["Datenbank"]

    def check_user(self, uid):
        """
        Prüft, ob ein User in der DB existiert
        :param uid:
        :return:
        """
        db = Database()
        res = db.check_if_exist("users", self.config_db['PATH'], "uid", uid)
        if res:
            self.logger.info("[USER CHECK] User mit der UID: %s - existiert bereits!", self.uid)
            return False
        else:
            self.logger.info("[USER CHECK] Nutzer mit der ID: %s existiert noch nicht! -> User wird gespeichert..",
                             self.uid)
            return True

    def new_user(self, userdata):
        """
        Anlegen eines neuen Users in der DB
        :param userdata:
        :return:
        """
        query = "INSERT INTO users (uid, name, chatid) values ({}, '{}', {})".format(
            userdata[0], userdata[1], userdata[2])
        self.db.execute_db(query, self.config_db['PATH'])
        self.logger.info("[NEW USER] Nutzer wurde erfolgreich mit der ID: %s angelegt!", self.uid)

    def del_user(self, id):
        """
        User aus der DB löschen
        :param id:
        :return:
        """
        query = "DELETE FROM users WHERE id={}".format(id)
        self.db.execute_db(query, "warn.db")
        self.logger.info("[DELETE USER] Nutzer wurde erfolgreich mit der ID: %s gelöscht!", self.uid)

    def edit_user(self, data):
        """
        User bearbeiten und in der DB speichern
        :param data:
        :return:
        """
        # 4 ist die Gruppe
        if data[4] == "None":  # Gruppe None
            query = "UPDATE users SET name='{}', lang='{}', pref_location='{}', warnings='{}' WHERE id={}".format(
                data[1], data[2], data[6], data[5],
                data[0])
        else:
            if data[4] == "": # Gruppe leer
                query = "UPDATE users SET name='{}', lang='{}', group_id=NULL, pref_location='{}', warnings='{}' WHERE id={}".format(
                    data[1], data[2], data[6], data[5],
                    data[0])
            else:
                query = "UPDATE users SET name='{}', lang='{}', group_id={},  pref_location='{}', warnings='{}' WHERE id={}".format(
                    data[1], data[2],
                    data[4], data[6], data[5], data[0])
        print(query)
        self.db.execute_db(query, "warn.db")
        self.logger.info("[UPDATE USER] Nutzer wurde erfolgreich mit der ID: %s geupdated!", self.uid)

    def get_user_info(self, uid):
        """
        Ruft die Infos zum User mit der uid ab.
        :param uid:
        :return:
        """
        results = []
        res = self.db.get_query("users", "UID=" + str(uid))
        for i in res:
            results.append(str(i[0]) + ": " + str(i[1]) + " (" + str(i[2]) + ")")

        return results

    def get_all_users(self):
        """
        Ruft alle User aus der DB ab
        :return:
        """
        results = []
        res = self.db.get_query("users")
        for i in res:
            results.append(str(i[0]) + ": " + str(i[1]) + " (" + str(i[2]) + ")")

        return results
