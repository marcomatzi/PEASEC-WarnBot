"""
    Diese Klasse dient zur verwaltung für die Nutzer.
    Eintragen in die DB sowie versenden von Nachrichten
    -> Dauerhafte Ausführung der Module im Loop
"""
import db_functions
from db_functions import Database
import logging


class Users:
    def __init__(self, userdata):
        self.uid = userdata
        self.logger = logging.getLogger(__name__)
        self.db = Database()

    def check_user(self, uid):
        db = Database()
        res = db.check_if_exist("users", "warn.db", "uid", uid)
        if res:
            self.logger.info("[USER CHECK] User mit der UID: %s - existiert bereits!", self.uid)
            return False
        else:
            self.logger.info("[USER CHECK] Nutzer mit der ID: %s existiert noch nicht! -> User wird gespeichert..", self.uid)
            return True

    def new_user(self, userdata):
        query = "INSERT INTO users (uid, name, chatid) values ({}, '{}', {})".format(
            userdata[0], userdata[1], userdata[2])
        self.db.execute_db(query, "warn.db")
        self.logger.info("[NEW USER] Nutzer wurde erfolgreich mit der ID: %s angelegt!", self.uid)

