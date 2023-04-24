
![Logo](https://raw.githubusercontent.com/marcomatzi/PEASEC-WarnBot/main/images/logo_f.png)

# PEASEC-WarnBot
Gemäß meiner Bachelorarbeit habe ich eine Implementierung des WarnBots in Telegram (IM) vorgenommen, wobei die TelegramAPI verwendet wurde. Das Ziel besteht darin, Warnmeldungen zu verschiedenen Themen, einschließlich Krieg und Katastrophen, Kriminalität, Verkehr, Gesundheit und Wetter, per Direktnachricht an den Nutzer zu senden.

Dieses Tool ist kein vollimplementierter Bot, sondern dient zu Evaluierungszwecken.



## Features

- Sammeln von Warnmeldungen aus der NINA-API
- Erstellung von eigenen Warnmeldungn (Custom-Warnungen)
- Erstellung von Benutzergruppen
- Versenden von Warnmeldungen über einen Telegram-Bot
    - Parameter für Evaluierung
        - Persönlichkeit des Bots (Anrede)
        - Versenden an Einzelperson oder Gruppen
        - Warnmeldung auswählen und bearbeiten
    - Versenden von Textnachrichten
- Einsehen von ein- und ausgehenden Nachrichten (gefiltert)
- Ausgeben von Notfallnummern
- Ausgeben von Notfalltipps
- Befehle im Chat
- Tastatur im Chat



## Installation

Das Programm wurde in Python 3.9 entwickelt und getestet.

Um den WarnBot in Telegram zu verwenden, muss im Vorfeld ein Bot über den Botfather (https://telegram.me/BotFather) erstellt werden. Der Botfather ist ein Service, der die Erstellung von Bots in Telegram vereinfacht.

1) Laden Sie das Repository herunter oder klonen Sie es mit Git.
```php
  git clone https://github.com/marcomatzi/PEASEC-WarnBot.git
```
2) Installieren Sie die erforderlichen Pakete mit pip.
```php
  pip install -r requirements.txt
```    
3) Fügen Sie den BOT-KEY in die config.ini ein.
```php
  ...
  [TelegramAPI]
    KEY = abc:000
    ...
``` 
4) Programm ausführen mit
```php
  python main.py
```   
\
INFO:\
OPTIONAL 3.1) Falls Sie eine neue Datenbank ohne Inhalt verwenden möchten, können Sie die bestehende *.db löschen und den folgenden Befehl auführen.
```php
  python init.py
```  
Damit wird eine neue Datenbank erstellt, mit dem Namen aus der config.ini (Abschnitt Datenbank: PATH)
Wichtig: init.py muss vor der main.py ausgeführt werden.


## FAQ

#### Kann der Bot Warnmeldungen automatisch versenden?
Nein.

#### Welche Benutzerdaten sammelt der Bot?
Der Bot sammelt nur UserID, ChatID und Username. Im Setup kann der User noch Warnmeldungsarten und eine/n Region/Ort hinterlegen.

#### Welche Schnittstelle von Telegram wird genutzt?
Der Bot nutzt die URLs der API. Es wurde auf die Nutzung der TelegramBot-PY verzichtet.

#### Wo kann ich den Bot-KEY ändern?
In der config.ini sind alle relevanten Einstellungen hinterlegt. Dort können einfach die aktuellen Daten des Bots eingespeichert werden. (Abschnitt [TelegramAPI])

#### Wie kann ich eine andere DB verwenden?
Sie können über die init.py eine leere Datenbank erstellen. Dazu einfach in der confi.ini, im Abschnitt [Datenbank], einen neuen Namen bei PATH hinterlegen.

#### Wo kann ich das Intervall für die NINA-API ändern?
In der confi.ini im Abschnitt [WarnAppsAPI] und dann INTERVALL. Die Angabe bezieht sich auf Sekunden.

#### In der Datenbank sind keine Notfalltipps vorhanden?
Führe die Funktion "collect_notfalltipps" in collector.py aus. Diese lädt alle Infos aus der Nina API.

#### Gibt es eine Prefilled Datenbank?
Ja! Nutze dazu die warn_prefilled.db. Zur Nutzung den Namen in warn.db oder in der condig.ini den Datenbanknamen ändern.



## Used By

Das Projekt wird von folgenden Unternehmen/Gruppen genutzt:

- PEASEC – Wissenschaft und Technik für Frieden und Sicherheit (TU Darmstadt)


## Support

Für Support email marco@matissek.com oder [@marcomatzi](https://www.github.com/marcomatzi).


## Acknowledgements

 - [tkinter](https://docs.python.org/3/library/tkinter.html)
 - [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
 - [sqllite3](https://sqlite.org/index.html)
 - [Pillow](https://pillow.readthedocs.io/en/stable/)
 - [requests](https://pypi.org/project/requests/)
 - [Python](https://www.python.org/)

## Screenshots

![App Screenshot](https://raw.githubusercontent.com/marcomatzi/PEASEC-WarnBot/main/screenshots/Screenshot_home.png)
![App Screenshot](https://raw.githubusercontent.com/marcomatzi/PEASEC-WarnBot/main/screenshots/Screenshot_eval.png)
![App Screenshot](https://raw.githubusercontent.com/marcomatzi/PEASEC-WarnBot/main/screenshots/Screenshot_usergroup.png)
![App Screenshot](https://raw.githubusercontent.com/marcomatzi/PEASEC-WarnBot/main/screenshots/Screenshot_warning.png)


## Authors

- [@marcomatzi](https://www.github.com/marcomatzi)



