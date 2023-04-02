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
        # Data1 ist der aktulle Stand (JSON)
        # Data2 ist der Remote stand (JSON)
        try:
            with open(data1, "r") as f1:
                data1 = f1.read()
        except:
            return str(data1) + ": Datei konnte nicht gelesen werden."

        if str(data1) == str(data2):
            return True  # gleich
        else:
            return False  # ungleich

    def catch_warnings(self, offset):
        api_urls = [
            ['KAT', 'https://nina.api.proxy.bund.dev/api31/katwarn/mapData.json'],  # Katwarn Meldungen
            ['BIW', 'https://nina.api.proxy.bund.dev/api31/biwapp/mapData.json'],  # Biwapp Meldungen
            ['MOW', 'https://nina.api.proxy.bund.dev/api31/mowas/mapData.json'],  # Mowas Meldungen
            ['DWD', 'https://nina.api.proxy.bund.dev/api31/dwd/mapData.json'],  # DWD Meldungen
            # ['LHP', 'https://nina.api.proxy.bund.dev/api31/lhp/mapData.json'],
            # LHP (Länderübergreifenden Hochwasserportals) Meldungen
            ['POL', 'https://nina.api.proxy.bund.dev/api31/police/mapData.json']  # Polizei Meldungen
        ]
        params = {
            "timeout": 100,
            "offset": offset
        }
        # TODO: Vergleich nach Updates muss anders gemacht werden, weil die API kein Timestamp liefert.
        #  Webhook nutzen?
        self.get_warning_information("kat.64275c6362aefd2bb0bb6bb8_public_topics", 1)
        self.check_exist_json(api_urls)
        while True:
            print("[" + str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + "] CHECK WARNING UPDATES..")
            for url in api_urls:
                print("\t[" + str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + "] " + url[0] + " checked.")
                response = requests.get(f"{url[1]}", params)

                if response.status_code == 200:
                    updates = response.json()
                    if updates and len(updates) > 0:
                        res_comp = self.compare_json_files(self.path_json + url[0] + ".json", updates)

                        if not res_comp:  # Wenn Die Dateien unterschiedlich waren vom Content
                            self.process_information(updates)
                            self.write_in_json(updates, url[0])
                    else:
                        self.write_in_json("", url[0])
                else:
                    print(response.status_code)

            time.sleep(59)  # Excecute every 59sec + 1sec startup time (every 60 sec checker)

    def update_warning(self):
        pass

    import json

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
            m_descr = ''.replace("'", "''")
            m_geo = ''.replace("'", "''")

            if "de" in m_title:
                m_title_de = m_title['de'].replace("'", "''")
            if "en" in m_title:
                m_title_en = m_title['en'].replace("'", "''")

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
                        "\t\t[updater_warnings][" + m_last_update + "]" + m_id + " wurde aktualisiert! (New Version: " + str(
                            m_version) + ") prev: " + str(db_check_result[4]))
                    # query = "UPDATE warnings SET title_de = '{}', title_en = '{}' , version  = {}, severity  = '{}'," \
                    #        " descr = '{}', last_update = '{}' WHERE wid = '{}' ".format(m_title_de, m_title_en,
                    #                                                                     m_version, m_severity, m_descr,
                    #                                                                     m_last_update, m_id)

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
                    self.get_warning_information(m_id, m_version)
            else:
                print(
                    "\t\t[insert_warnings][" + m_last_update + "]" + m_id + " wurde angelegt! (Version: " + str(
                        m_version) + ")")
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
                self.get_warning_information(m_id, m_version)

    def force_update_info(self):
        # SELECT-Abfrage ausführen, um die wid-Spalte aus der Tabelle warnings abzurufen
        results = Database.get_query("warnings")

        # Alle Ergebnisse aus der Abfrage abrufen

        # Jedes Element an die Funktion process_warning() übergeben
        i = 1
        for row in results:
            print(str(i) + "/" + str(len(results)) + " - ")
            self.get_warning_information(row[1], row[4])
            i += 1

    def get_warning_information(self, wid, ver):
        url = "https://nina.api.proxy.bund.dev/api31/warnings/{}.json".format(wid)
        response = requests.get(f"{url}", {"timeout": 100})

        if response.status_code == 200:
            data = response.json()

            # Laden des JSON-Objekts als Python-Datenstruktur

            for d in data:
                dataInfo = data['info']
                dataInfo = dataInfo[0]
                json_data = json.dumps(dataInfo)
                dataInfo2 = json.loads(json_data)

                # print(str(d) + ': ' + str(data[d]))

            self.write_db_information(wid, ver, data['sender'], data['status'], data['msgType'], data['scope'],
                                      dataInfo2.get("event", ""), dataInfo2.get("urgency", ""),
                                      dataInfo2.get("severity", ""), dataInfo2.get("effective", ""),
                                      dataInfo2.get("senderName", ""),
                                      dataInfo2.get("headline", ""), dataInfo2.get("description", ""),
                                      dataInfo2.get("web", ""),
                                      dataInfo['area'][0]['areaDesc'], dataInfo2.get("instruction", ""),
                                      dataInfo2.get("certainty", ""), dataInfo2.get("onset", ""),
                                      dataInfo2.get("expires", ""))

            """
            for d in data:
                if str(d) == "info":
                    for di in data['info']:
                        data2 = data['info']
                        dictionary = {"Name": data2[0], "Alter": eintrag[1], "Stadt": eintrag[2]}
                        data_array.append({str(di), str(data2[di])})
                data_array.append({str(d), str(data[d])})
            """
        else:
            pass
            #print(response.status_code)

        # query = ""
        # Database.execute_db(query, self.__DB)

    def write_db_information(self, wid, ver, sender, status, msgType, scope, event, urgency, severity, effective,
                             senderName, headline, desc, web, area, instruction, certainty, onset, expires):
        query = "INSERT INTO warning_information (wid,version,sender,status,msgType,scope,senderName,headline,text,web,areaDesc,geo,image,event,urgency, severity, certainty, DateEffective,DateOnset,DateExpires,instruction)" \
                "VALUES ('{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            wid, ver, sender, status, msgType, scope, senderName, headline, desc, web, area,
            "GEO_DATA", self.get_logo(sender), event, urgency, severity, certainty, effective, onset, expires,
            instruction)
        Database.execute_db(query, self.__DB)

    def get_logo(self, sender) -> str:
        # TODO: Event codes noch hinzufügen!
        url = "https://nina.api.proxy.bund.dev/api31/appdata/gsb/logos/logos.json"
        response = requests.get(f"{url}", {"timeout": 100})

        if response.status_code == 200:
            data = response.json()

            json_data = json.dumps(data)
            data = json.loads(json_data)
            for d in data['logos']:
                print(d)
                if str(sender) in d['senderId']:
                    img = d['image']
                    print("https://nina.api.proxy.bund.dev/api31/appdata/gsb/logos/{}".format(img))
                    return "https://nina.api.proxy.bund.dev/api31/appdata/gsb/logos/{}".format(img)
        else:
            print(response.status_code)

    def point_in_polygon(self, polygon: list, point: tuple) -> bool:
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def point_in_linestring(self, linestring: list, point: tuple) -> bool:
        # Eine LineString ist kein Polygon und kann deshalb nicht geprüft werden.
        return False

    def point_in_multipoint(self, multipoint: list, point: tuple) -> bool:
        # Überprüfen, ob das Point-Objekt in der Liste der MultiPoint-Koordinaten enthalten ist.
        return point in multipoint

    def point_in_multilinestring(self, multilinestring: list, point: tuple) -> bool:
        # Eine MultiLineString ist kein Polygon und kann deshalb nicht geprüft werden.
        return False

    def point_in_multipolygon(self, multipolygon: list, point: tuple) -> bool:
        for polygon in multipolygon:
            if self.point_in_polygon(polygon[0], point):
                return True
        return False

    def point_in_geojson(self, geojson: dict, point: tuple) -> bool:
        if geojson["type"] == "Point":
            return point == tuple(geojson["coordinates"])
        elif geojson["type"] == "LineString":
            return self.point_in_linestring(geojson["coordinates"], point)
        elif geojson["type"] == "Polygon":
            return self.point_in_polygon(geojson["coordinates"][0], point)
        elif geojson["type"] == "MultiPoint":
            return self.point_in_multipoint(geojson["coordinates"], point)
        elif geojson["type"] == "MultiLineString":
            return self.point_in_multilinestring(geojson["coordinates"], point)
        elif geojson["type"] == "MultiPolygon":
            return self.point_in_multipolygon(geojson["coordinates"], point)


if __name__ == "__main__":
    server = f'https://warnung.bund.de/api31'
    db = "warn.db"
    c = Collector(server, db)
    c.force_update_info()

"""server = f'https://warnung.bund.de/api31'
db = "warn.db"
c = Collector(server, db)
c.catch_warnings(None)"""
