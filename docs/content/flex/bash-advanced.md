---
title: Bash Advanced
created: 2026-11-17 13:04:56 +0100
last_modified: 2026-11-23 10:17:22 +0100
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

| Command                            | Functie                                          |
|------------------------------------|--------------------------------------------------|
| `echo "Another line" >> hello.txt` | Voeg **text** toe aan het **einde** van een file |
| `date >> today.txt`                | Voeg **output van een command** toe aan het **einde** van een file |

## Oefeningen 

**Mijn eerste tekstbestand**
1. Maak een bestand persoonlijk.txt met daarin je naam en 2 lijnen andere informatie over jezelf, elk op een eigen lijn.
2. Voeg de tekst 'Ik leer werken met Bash' toe aan persoonlijk.txt, zonder de bestaande inhoud te overschrijven.

# Bash advanced commands

| Command                                  | Afkorting / Betekenis       | Functie                                                   |
|------------------------------------------|-----------------------------|-----------------------------------------------------------|
| `date`                                   | Date                             | De huidige datum en tijd weergeven                        |
| `date +%F`                               | Date                        | De huidige datum weergeven (YYYY-MM-DD)                   |
| `whoami`                                 | Who am I                    | De naam van de huidige gebruiker weergeven                |
| `grep "woord" file.txt`                  | Global Regular Expression Print | Zoeken naar tekst in een bestand                      |
| `grep -c "woord" file.txt`               | Count                       | Het aantal regels met een bepaalde tekst tellen           |
| `grep -o "woord" file.txt`               | Only matching               | Enkel de gevonden overeenkomsten weergeven                |
| `sort`                                   | Sort                             | Tekst alfabetisch of numeriek sorteren                    |
| `uniq`                                   | Unique                      | Opeenvolgende dubbele regels verwijderen                  |
| `wc`                                     | Word Count                  | Het aantal regels, woorden en tekens tellen               |
| `wc -l`                                  | Word Count - Lines          | Het aantal regels tellen                                  |
| `head -n 5`                              |                             | De eerste 5 regels weergeven                              |
| `tail -n 5`                              |                             | De laatste 5 regels weergeven                             |
| `du -ah .`                               | Disk Usage                  | De grootte van bestanden en mappen weergeven              |

**Dagboek**
1. Maak een bestand dagboek.txt met de datum van vandaag en op een 2e lijn de tekst 'Vandaag heb ik Bash geleerd'.

**Mijn computer**
Gebruik de juiste commando's om de volgende informatie telkens in een afzonderlijk bestand op te slaan:
1. De inhoud van de huidige map in bestanden.txt.
2. De huidige locatie in locatie.txt.
3. De huidige datum in datum.txt.
4. De gebruikersnaam waarmee je bent ingelogd in gebruiker.txt

