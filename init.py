import configparser

from db_functions import Database
from collector import Collector
import sqlite3


class SetupEnv:
    """    config = configparser.ConfigParser()
        config.read("config.ini")
        config_db = config["Datenbank"]
        # Verbindung zur Datenbank herstellen (wenn die Datenbank noch nicht existiert, wird sie erstellt)
        conn = sqlite3.connect(config_db['PATH'])

        # Verbindung schließen
        conn.close()"""

    print("Umgebung wird initialisiert...")
    db = Database()
    db.create_db()
    print("Datenbank wurde erstellt!")

    sql_list = [
        ('Katwarn', 'kat'),
        ('Biwapp', 'kat'),
        ('Mowas', 'kat'),
        ('DWD', 'Wetter'),
        ('Hochwasser Portal', 'kat'),
        ('Polizei', 'kat'),
        ('Covid', 'Covid')
    ]
    db.insert_multiple(sql_list, "warn.db")

    print("Fertig! Init abgeschlossen...")