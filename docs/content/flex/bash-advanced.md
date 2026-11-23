---
title: Bash Advanced
created: 2026-11-17 13:04:56 +0100
last_modified: 2026-11-23 11:00:00 +0100
---

# Add text to files

## `>` Write to file

Als de file nog niet bestaat, zal deze automatisch aangemaakt worden.

| Command                                                                               | Functie                                   |
|---------------------------------------------------------------------------------------|-------------------------------------------|
| `echo "Hello world" > hello.txt`                                                      | Schrijf **text** naar een file            |
| `printf "Hello world\n" > hello.txt`                                                  | Schrijf **text met enters** naar een file |
| `ls > files.txt`<br>`pwd > location.txt`<br>`date > today.txt`<br>`whoami > user.txt` | Schrijf de **output van een command**     |

## `>>` Append to file 

| Command                            | Functie                                                            |
|------------------------------------|--------------------------------------------------------------------|
| `echo "Another line" >> hello.txt` | Voeg **text** toe aan het **einde** van een file                   |
| `date >> today.txt`                | Voeg **output van een command** toe aan het **einde** van een file |

### Oefeningen 

**Mijn eerste tekstbestand**
1. Maak een bestand persoonlijk.txt met daarin je naam en 2 lijnen andere informatie over jezelf, elk op een eigen lijn.
2. Voeg de tekst 'Ik leer werken met Bash' toe aan persoonlijk.txt, zonder de bestaande inhoud te overschrijven.

# Bash advanced commands

| Date & Time      | Functie                                              |
|------------------|------------------------------------------------------|
| `date`           | De huidige datum en tijd weergeven                   |
| `date +%F`       | De huidige datum weergeven (YYYY-MM-DD)              |
| `date %d`        | Dag van de maand                                     |
| `date %m`        | Maand                                                |
| `date %Y`        | Volledig jaartal                                     |
| `date %y`        | Verkort jaartal                                      |
| `date %H`        | Uur                                                  |
| `date %M`        | Minuten                                              |
| `date %S`        | Seconden                                             |
| `date %A`        | Volledige naam van de weekdag                        |
| `date %B`        | Volledige naam van de maand                          |
| `date +%d-%m-%Y` | De huidige datum weergeven in het formaat DD-MM-YYYY |
| `date +%H:%M:%S` | Het huidige uur weergeven in het formaat UU:MM:SS    |
| `date +%H:%M`    | Het huidige uur weergeven in het formaat UU:MM       |

### Oefeningen

**Dagboek**
1. Maak een bestand dagboek.txt met de datum van vandaag.
2. Voeg op de tweede lijn de tekst Vandaag heb ik Bash geleerd toe.
3. Voeg een derde lijn toe met het huidige tijdstip en de tekst Het is me gelukt om het tijdstip toe te voegen.

| Command                    | Afkorting / Betekenis           | Functie                                         |
|----------------------------|---------------------------------|-------------------------------------------------|
| `whoami`                   | Who am I                        | De naam van de huidige gebruiker weergeven      |
| `grep "woord" file.txt`    | Global Regular Expression Print | Zoeken naar tekst in een bestand                |
| `grep -c "woord" file.txt` | Count                           | Het aantal regels met een bepaalde tekst tellen |
| `sort`                     | Sort                            | Tekst alfabetisch of numeriek sorteren          |
| `uniq`                     | Unique                          | Opeenvolgende dubbele regels verwijderen        |
| `wc`                       | Word Count                      | Het aantal regels, woorden en tekens tellen     |
| `wc -l`                    | Word Count: Lines               | Het aantal regels tellen                        |
| `wc -w`                    | Word Count: Words               | Het aantal regels tellen                        |
| `wc -m`                    | Word Count: | Het aantal regels tellen                        |
| `head -n 5`                |                                 | De eerste 5 regels weergeven                    |
| `tail -n 5`                |                                 | De laatste 5 regels weergeven                   |
| `du -ah .`                 | Disk Usage                      | De grootte van bestanden en mappen weergeven    |

### Oefeningen

**Mijn computer**
Gebruik de juiste commando's om de volgende informatie telkens in een afzonderlijk bestand op te slaan:
1. De inhoud van de huidige map in bestanden.txt.
2. De huidige locatie in locatie.txt.
3. De huidige datum in datum.txt.
4. De gebruikersnaam waarmee je bent ingelogd in gebruiker.txt

**Fruit**
1. Maak een bestand aan met deze tekst:
```txt 
appel
banaan
appel
kers
druif
banaan
appel
mango
kers
appel
```
2. Zoek alle regels waarin appel voorkomt.
3. Tel hoeveel regels het woord appel bevatten.
4. Hoeveel regels bevat fruit.txt?
5. Hoeveel woorden bevat het bestand?
6. Hoeveel tekens bevat het bestand?
7. Toon het fruit gesorteerd.
8. Sla het gesorteerde fruit op (overschrijf het bestand).
9. Verwijder dubbele opeenvolgende regels en overschrijf het bestand.
