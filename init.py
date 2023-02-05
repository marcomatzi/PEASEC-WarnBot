from db_functions import Database
from collector import Collector

class SetupEnv:
    print("Umgebung wird initialisiert...")
    db = Database()
    """
    db.create_db()
    print("Datenbank wurde erstellt!")
    print("Fertig! Init abgeschlossen...")

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
    """
    # db.insert_into("Insert into warntype (name, type) values ('Test', 'test')", "warn.db")
    #db.get_query("warntype")

    db.get_query("warnings")
    Collector.custom_warning("custom.8477464840_public_topics", "Ich habe durst", "I am thirsty", 1, "low", "Alert", "", "Custom", "Ich brauche ein Getränk.")
    db.get_query("warnings")
    # db.delete_query("Delete from warntype where name='Test'", "warn.db")
    # db.get_query("warntype")
