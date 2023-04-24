
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
        - Versenden an Einzelperson oder Gruppe
        - Warnmeldung auswählen und bearbeiten
    - Versenden von Textnachrichten
- Einsehen von ein- und ausgehenden Nachrichten (gefiltert)
- Ausgeben von Notfallnummern
- Ausgeben von Notfalltipps
- Befehle im Chat
- Tastatur im Chat



## FAQ

#### Kann der Bot Warnmeldungen automatisch versenden?
Nein.

#### Welche Benutzerdaten sammelt der Bot?
Der Bot sammelt nur UserID, ChatID und Username. Im Setup kann der User noch Warnmeldungsarten und eine/n Region/Ort hinterlegen.

#### Welche Schnittstelle von Telegram wird genutzt?
Der Bot nutzt die URLs der API. Es wurde auf die Nutzung der TelegramBot-PY verzichtet.

#### Wo kann ich die DB und den Bot-KEY ändern?
In der config.ini sind alle relevanten Einstellungen hinterlegt. Dort können einfach die aktuellen Daten des Bots eingespeichert werden.


## Installation

Das Programm wurde in Python 3.9 entwickelt und getestet.

Laden Sie das Repository herunter oder klonen Sie es mit Git.
```php
  git clone https://github.com/marcomatzi/PEASEC-WarnBot.git
```
Installieren Sie die erforderlichen Pakete mit pip.
```php
  pip install -r requirements.txt
```    
Fügen Sie den BOT-KEY in die config.ini ein.
```php
  ...
  [TelegramAPI]
    KEY = abc:000
    ...
``` 
Programm ausführen mit
```php
  python main.py
```   
\
INFO:\
Falls Sie die warn.db nicht verwenden möchten, können Sie diese aus dem Ordner löschen oder umbenennen und eine neue generieren mit:
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

![App Screenshot](https://raw.githubusercontent.com/marcomatzi/PEASEC-WarnBot/main/screenshots/Screenshot_home.png)
![App Screenshot](https://raw.githubusercontent.com/marcomatzi/PEASEC-WarnBot/main/screenshots/Screenshot_eval.png)
![App Screenshot](https://raw.githubusercontent.com/marcomatzi/PEASEC-WarnBot/main/screenshots/Screenshot_usergroup.png)
![App Screenshot](https://raw.githubusercontent.com/marcomatzi/PEASEC-WarnBot/main/screenshots/Screenshot_warning.png)


## Authors

- [@marcomatzi](https://www.github.com/marcomatzi)



