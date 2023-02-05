"""
    Sammeln der Daten aus NINA usw
"""
from db_functions import Database

class Collector:
    def __init__(self, api, server, db):
        self.__API = api
        self.__Server = server
        self.__DB = db

    @staticmethod
    def custom_warning(wid, title_de, title_en, version, severity, type, geo, source, descr):
        db = Database()
        res = db.check_if_exist("warnings", "warn.db", "wid", wid)
        if res:
            query = "UPDATE warnings SET version={}, severity='{}', descr ='{}' WHERE wid='{}'".format(version, severity, descr, wid)
        else:
            query = "INSERT INTO warnings (wid,title_de,title_en,version,severity,type,geo,source, descr) values ('{}','{}','{}',{},'{}','{}','{}','{}', '{}')".format(wid, title_de, title_en, version, severity, type, geo, source, descr)

        Database.execute_db(query, "warn.db")

    def catch_warnings(self):
        pass

    def update_warning(self):
        pass
