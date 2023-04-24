
![Logo](https://raw.githubusercontent.com/marcomatzi/PEASEC-WarnBot/main/images/logo_f.png)

# PEASEC-WarnBot
Implementation meiner Bachelorarbeit - WarnBot Implementierung in Telegram (IM) mit Verwendung der TelegramAPI. Sendet Warnmeldungen an den Nutzer per Direktnachricht in Telegram, wie beispielsweise Krieg und Katastrophen, sondern auch Kriminalitäts-, Verkehrs-, Gesundheits- und Wetterwarnungen.

Dieses Tool ist kein vollimplementierter Bot, sondern dient zu Evaluierungszwecke.



## Features

- Sammeln von Warnmeldungen aus der NINA-API
- Erstellung von eigenen Warnmeldung (Custom-Warnungen)
- Erstellen von Benutzergruppen
- Versenden von Warnmeldungen über einen Telegram-Bot
    - Parameter für Evaluierung
        - Persönlichkeit des Bots (Anrede)
        - Versenden an Einzelperson oder Gruppe
        - Warnmeldung auswählen und bearbeiten
    - Versenden von Text
- Einsehen von Ein- und Ausgehenden Nachrichten (gefiltert)
- Ausgeben von Notfallnummern
- Ausgeben von Notfalltipps
- Befehle im Chat
- Tastatur im Chat




## FAQ

#### Kann der Bot Warnmeldungen automatisch versenden?
Nein.

#### Welche Benutzerdaten sammelt der Bot?
Der Bot sammelt nur UserID, ChatID und Username. Im Setup kann der User noch Warnmeldungsarten und eine/n Ort/Region hinterlegen.

#### Welche Schnittstelle für zu Telegram genutzt?
Der Bot nutzt die URLs der API. Es wurde auf die Nutzung der TelegramBot-PY verzichtet.

#### Wo kann ich die DB und den Bot-KEY ändern?
In der config.ini sind alle relevanten Einstellungen hinterlegt. Dort können einfach die aktuellen Daten des Bots eingespeichert werden.


## Installation

Das Programm wurde mit Python 3.9 Entwickelt und getestet

Laden Sie das Repository herunter oder klonen Sie es mit Git.
```php
  git clone https://github.com/marcomatzi/PEASEC-WarnBot.git
```
Installieren Sie die erforderlichen Pakete mit pip.
```php
  pip install -r requirements.txt
```    
Programm ausführen mit
```php
  python main.py
```   
\
INFO:\
Falls Sie die warn.db nicht verwenden möchten, können Sie die aus dem Ordner löschen oder Umbenenn und eine neue Generieren mit:
```php
  python init.py
```  
## Used By

Das Projekt wird von folgenden Unternehmen/Gruppen genutzt:

- PEASEC – Wissenschaft und Technik für Frieden und Sicherheit (TU Darmstadt)


## Support

Für Support, email marco@matissek.com oder [@marcomatzi](https://www.github.com/marcomatzi).


## Acknowledgements

 - [tkinter](https://de.wordpress.org/download/)
 - [customtkinter](https://www.php.net/)
 - [sqllite3](https://www.mysql.com/de/)
 - [PIL](https://www.mysql.com/de/)
 - [Python](https://www.mysql.com/de/)

## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Authors

- [@marcomatzi](https://www.github.com/marcomatzi)



