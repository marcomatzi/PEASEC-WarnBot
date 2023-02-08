"""
    Sammeln der Daten aus NINA usw
"""
import requests
import time
from db_functions import Database
from datetime import datetime
import os
import json
import logging


class Collector:
    def __init__(self, server, db):
        self.__Server = server
        self.__DB = db
        self.path_json = os.path.dirname(__file__) + "/last_updates/"

    @staticmethod
    def custom_warning(wid, title_de, title_en, version, severity, type, geo, source, descr):
        db = Database()
        res = db.check_if_exist("warnings", "warn.db", "wid", wid)
        if res:
            query = "UPDATE warnings SET version={}, severity='{}', descr ='{}' WHERE wid='{}'".format(version,
                                                                                                       severity, descr,
                                                                                                       wid)
        else:
            query = "INSERT INTO warnings (wid,title_de,title_en,version,severity,type,geo,source, descr) values ('{}','{}','{}',{},'{}','{}','{}','{}', '{}')".format(
                wid, title_de, title_en, version, severity, type, geo, source, descr)

        Database.execute_db(query, "warn.db")

    def check_exist_json(self, list_of_files):
        path = os.path.dirname(__file__) + "/last_updates/"
        for f in list_of_files:

            f_path = path + f[0] + ".json"

            if not os.path.exists(f_path):
                with open(f_path, "w") as file:
                    file.write("")
                print("File " + f_path + " wurde erstellt!")

    def write_in_json(self, data, f):

        f_path = self.path_json + f + ".json"
        with open(f_path, "w") as file:
            file.write(str(data))

    def compare_json_files(self, data1, data2):
        try:
            with open(data1, "r") as f1:
                data1 = f1.read()
        except:
            return str(data1) + ": Datei konnte nicht gelesen werden."
        if str(data1) == str(data2):
            return True     # gleich
        else:
            return False    # ungleich

    def catch_warnings(self, offset):
        api_urls = [
            ['KAT', 'https://nina.api.proxy.bund.dev/api31/katwarn/mapData.json'],  # Katwarn Meldungen
            ['BIW', 'https://nina.api.proxy.bund.dev/api31/biwapp/mapData.json'],  # Biwapp Meldungen
            ['MOW', 'https://nina.api.proxy.bund.dev/api31/mowas/mapData.json'],  # Mowas Meldungen
            ['DWD', 'https://nina.api.proxy.bund.dev/api31/dwd/mapData.json'],  # DWD Meldungen
            ['LHP', 'https://nina.api.proxy.bund.dev/api31/lhp/mapData.json'],
            # LHP (Länderübergreifenden Hochwasserportals) Meldungen
            ['POL', 'https://nina.api.proxy.bund.dev/api31/police/mapData.json']  # Polizei Meldungen
        ]
        params = {
            "timeout": 100,
            "offset": offset
        }
        # TODO: Vergleich nach Updates muss anders gemacht werden, weil die API kein Timestamp liefert.
        #  Webhook nutzen?

        self.check_exist_json(api_urls)
        while True:
            print("["+str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))+"] CHECK WARNING UPDATES..")
            for url in api_urls:
                response = requests.get(f"{url[1]}", params)

                if response.status_code == 200:
                    updates = response.json()
                    if updates and len(updates) > 0:
                        res_comp = self.compare_json_files(self.path_json+url[0]+".json", updates)

                        if not res_comp:
                            self.process_information(updates)
                            self.write_in_json(updates, url[0])
                    else:
                        self.write_in_json("", url[0])
                else:
                    print(response.status_code)

            time.sleep(60)

    def update_warning(self):
        pass

    def process_information(self, updates):
        m_last_update = datetime.now()
        m_last_update = m_last_update.strftime("%d-%m-%Y %H:%M:%S")

        print("[updater_warnings][" + m_last_update + "] Checker wird ausgeführt...")
        for u in updates:
            m_source = None
            m_title_de = None
            m_title_en = None

            m_id = u['id']
            m_version = str(u['version'])
            # m_startDate = u['startDate']
            # m_expiresDate = u['expiresDate']
            m_severity = u['severity']
            m_type = u['type']
            m_title = u['i18nTitle']
            m_descr = ''
            m_geo = ''

            if "de" in m_title:
                m_title_de = m_title['de']
            if "en" in m_title:
                m_title_en = m_title['en']

            if "kat" in m_id:
                m_source = "kat"
            elif "dwd" in m_id:
                m_source = "dwd"
            elif "lhp" in m_id:
                m_source = "lhp"
            elif "mow" in m_id:
                m_source = "mow"
            else:
                m_source = "unknown"

            db_check_result = Database.check_if_exist("warnings", self.__DB, "wid", m_id)
            if db_check_result:
                if (db_check_result[4] == m_version):
                    # print("[updater_warnings][" + m_last_update + "]" + m_id + " ist bereits auf der aktuellsten version!")
                    continue
                else:
                    print(
                        "[updater_warnings][" + m_last_update + "]" + m_id + " wurde aktualisiert! (New Version: " + m_version)
                    query = "UPDATE warnings SET title_de = '{}', title_en = '{}' , version  = {}, severity  = '{}'," \
                            " descr = '{}', last_update = '{}' WHERE wid = '{}' ".format(m_title_de, m_title_en,
                                                                                         m_version, m_severity, m_descr,
                                                                                         m_id, m_last_update)
                    Database.execute_db(query, self.__DB)
            else:
                print(
                    "[insert_warnings][" + m_last_update + "]" + m_id + " wurde angelegt! (Version: " + m_version)
                query = "INSERT INTO warnings (wid, title_de, title_en , version, severity, type, geo, source, descr, last_update) " \
                        "values ('{}', '{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}')".format(m_id, m_title_de,
                                                                                                   m_title_en,
                                                                                                   m_version,
                                                                                                   m_severity,
                                                                                                   m_type,
                                                                                                   m_geo, m_source,
                                                                                                   m_descr,
                                                                                                   m_last_update)
                Database.execute_db(query, self.__DB)


server = f'https://warnung.bund.de/api31'
db = "warn.db"
c = Collector(server, db)
c.catch_warnings(None)
