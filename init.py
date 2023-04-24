import configparser

from db_functions import Database
from collector import Collector
import sqlite3


class SetupEnv:
    config = configparser.ConfigParser()
    config.read("config.ini")
    config_db = config["Datenbank"]

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
    db.insert_multiple(sql_list, config_db['PATH'])

    print("Fertig! Init abgeschlossen...")