"""
    Diese Klasse dient zur verwaltung für die Gruppen mit Nutzern.
    Eintragen in die DB sowie versenden von Nachrichten
    -> Dauerhafte Ausführung der Module im Loop
"""
import db_functions
from db_functions import Database
import logging


class UserGroup:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = Database()
    def check_group(self, gnr):
        result = self.db.get_query("user_groups", "group_nr={}".format(gnr))
        if len(result) < 1:
            return False
        else:
            return True

    def create_group(self, gnr, gd):
        if not self.check_group(gnr):
            query = "INSERT INTO user_groups (group_nr, description) values ({}, '{}')".format(gnr, gd)
            self.db.execute_db(query, "warn.db")
            self.logger.info("[NEW GROUP] Gruppe wurde erfolgreich mit der Nr: %s angelegt!", gnr)
            return True
        else:
            self.logger.info("[NEW GROUP] Gruppe erstellen fehlgeschlagen!! Gruppe mit der Nr: %s existiert bereits!", gnr)
            return False


    def del_group(self, gnr):
        query = "DELETE FROM user_groups WHERE group_nr={}".format(gnr)
        self.db.execute_db(query, "warn.db")
        self.logger.info("[DEL GROUP] Gruppe mit der Nr. %s wurde erfolgreich gelöscht!", gnr)

    def edit_group(self, gnr, descr):
        query = "UPDATE user_groups SET group_nr={}, description='{}' WHERE group_nr={}".format(gnr, descr)
        self.db.execute_db(query, "warn.db")
        self.logger.info("[DEL GROUP] Gruppe mit der Nr. %s wurde erfolgreich gelöscht!", gnr)

    def get_group(self, gnr):
        return self.db.get_query("user_groups", "group_nr={}".format(gnr))

    def get_all_groups(self):
        res = self.db.get_query("user_groups")

        if len(res) < 1:
            results = ['n/A']
        else:
            results = []
            for i in res:
                results.append(str(i[0]) + ": " + str(i[1]) + " (" + str(i[2]) + ")")

        return results
