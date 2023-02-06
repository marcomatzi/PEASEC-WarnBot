"""
    Sammeln der Daten aus NINA usw
"""
import requests

from db_functions import Database
from datetime import datetime


class Collector:
    def __init__(self, server, db):
        self.__Server = server
        self.__DB = db

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

    def catch_warnings(self, offset):
        api_urls = [
            'https://nina.api.proxy.bund.dev/api31/katwarn/mapData.json',  # Katwarn Meldungen
            'https://nina.api.proxy.bund.dev/api31/biwapp/mapData.json',  # Biwapp Meldungen
            'https://nina.api.proxy.bund.dev/api31/mowas/mapData.json',  # Mowas Meldungen
            'https://nina.api.proxy.bund.dev/api31/dwd/mapData.json',  # DWD Meldungen
            'https://nina.api.proxy.bund.dev/api31/lhp/mapData.json',
            # LHP (Länderübergreifenden Hochwasserportals) Meldungen
            'https://nina.api.proxy.bund.dev/api31/police/mapData.json'  # Polizei Meldungen
        ]
        params = {
            "timeout": 100,
            "offset": offset
        }

        last_update_id = None
        for url in api_urls:
            response = requests.get(f"{url}", params)
            if response.status_code == 200:
                updates = response.json()
                if updates and len(updates) > 0:
                    self.process_information(updates)
                    # last_update_id = updates["result"][-1]["update_id"] + 1
                else:
                    last_update_id = None
            else:
                print(response.status_code)

    def update_warning(self):
        pass

    def process_information(self, updates):
        for u in updates:
            m_source = None
            m_title_de = None
            m_title_en = None

            m_id = u['id']
            m_version = u['version']
            # m_startDate = u['startDate']
            # m_expiresDate = u['expiresDate']
            m_severity = u['severity']
            m_type = u['type']
            m_title = u['i18nTitle']
            m_descr = ''
            m_geo = ''
            m_last_update = datetime.now()
            m_last_update = m_last_update.strftime("%d-%m-%Y %H:%M:%S")

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
                    print(m_id + " ist bereits auf der aktuellsten version!")
                    continue
                else:
                    query = "UPDATE warnings SET title_de = '{}', title_en = '{}' , version  = {}, severity  = '{}'," \
                            " descr = '{}' last_update = '{}' WHERE wid = '{}' ".format(m_title_de, m_title_en,
                                                                                        m_version, m_severity, m_descr,
                                                                                        m_id, m_last_update)
                    Database.execute_db(query, self.__DB)
            else:
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
