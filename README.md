
![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)

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
- Einsehen von Ein- und Ausgehenden Nachrichten
- Befehle im Chat
- Tastatur im Chat




## FAQ

#### Kann der Bot Warnmeldungen automatisch versenden?
Nein.

#### Welche Benutzerdaten sammelt der Bot?
Der Bot sammelt nur UserID, ChatID und Username.

#### Welche Schnittstelle für zu Telegram genutzt?
Der Bot nutzt die URLs der API. Es wurde auf die Nutzung der TelegramBot-PY verzichtet.


## Installation

Installation der Webseite benötigt man 
- PHP
- Apache
- MySQL / andere SQL
- WordPress API

INIT SQL:
```php
  DB.sql in MySQL Einfügen und ausführen
```
Template in Pfad einfügen:
```php
  wp-content/themes/
```    

theme-update-checker.php - Wird mit der Version im style.css abgeglichen
```php
  23  public $metadataUrl = 'URL/info.json';        //The URL of the theme's metadata file.
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



