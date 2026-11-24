---
title: Bash Advanced
created: 2026-11-17 13:04:56 +0100
last_modified: 2026-11-24 13:15:22 +0100
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

**Oefening: mijn eerste tekstbestand**

1. Maak een bestand persoonlijk.txt met daarin je naam en 2 lijnen andere informatie over jezelf, elk op een eigen lijn.
2. Voeg de tekst 'Ik leer werken met Bash' toe op een nieuwe lijn aan persoonlijk.txt, zonder de bestaande inhoud te overschrijven.

# Date & time

| Command          | Functie                                              |
|------------------|------------------------------------------------------|
| `date`           | De huidige datum en tijd weergeven                   |
| `date +%F`       | De huidige datum weergeven (YYYY-MM-DD)              |
| `date +%d`        | Dag van de maand                                     |
| `date +%m`        | Maand                                                |
| `date +%Y`        | Volledig jaartal                                     |
| `date +%y`        | Verkort jaartal                                      |
| `date +%H`        | Uur                                                  |
| `date +%M`        | Minuten                                              |
| `date +%S`        | Seconden                                             |
| `date +%A`        | Volledige naam van de weekdag                        |
| `date +%B`        | Volledige naam van de maand                          |
| `date +%d-%m-%Y` | De huidige datum weergeven in het formaat DD-MM-YYYY |
| `date +%H:%M:%S` | Het huidige uur weergeven in het formaat UU:MM:SS    |
| `date +%H:%M`    | Het huidige uur weergeven in het formaat UU:MM       |

**Oefening: dagboek**

1. Maak een bestand dagboek.txt met de datum van vandaag.
2. Voeg op de tweede lijn de tekst 'Vandaag heb ik Bash' geleerd toe.
3. Voeg een derde lijn toe met het huidige tijdstip en de tekst 'Het is me gelukt om het tijdstip toe te voegen'.

# System information

| Command           | Afkorting / Betekenis                       | Functie                                            |
|-------------------|---------------------------------------------|----------------------------------------------------|
| `whoami`          | Who am I                                    | De naam van de huidige gebruiker weergeven         |
| `du -ah file.txt` | Disk Usage<br>-a: All<br>-h: Human-readable | De grootte van een bestand weergeven               |
| `du -ah dir/`     | Disk Usage                                  | De grootte van alle bestanden in een dir weergeven |

**Oefening: mijn computer**

Gebruik de juiste commando's om de volgende informatie telkens in een afzonderlijk bestand op te slaan:
1. De inhoud van de huidige dir in bestanden.txt.
2. De huidige locatie in locatie.txt.
3. De volledige naam van de weekdag in datum.txt.
4. De gebruikersnaam waarmee je bent ingelogd in gebruiker.txt
5. Sla de grootte van alle bestanden en mappen in de huidige dir op in groottes.txt.

# Zoeken in een bestand

| Command                    | Afkorting / Betekenis            | Functie                                                     |
| `grep "woord" file.txt`    | Global Regular Expression Print  | Zoeken naar tekst in een bestand                            |
| `grep -c "woord" file.txt` | Count                            | Het aantal regels met een bepaalde tekst tellen             |
| `sort`                     | Sort                             | Tekst alfabetisch of numeriek sorteren                      |
| `uniq`                     | Unique                           | Opeenvolgende dubbele regels verwijderen                    |
| `wc`                       | Word Count                       | Het aantal regels, woorden en tekens tellen van een bestand |
| `wc -l`                    | Word Count: lines                | Het aantal **regels** tellen van een bestand                |
| `wc -w`                    | Word Count: words                | Het aantal **woorden** tellen van een bestand                 |
| `wc -m`                    | Word Count: multibyte characters | Het aantal **tekens** tellen van een bestand                |
| `head -n 5`                |                                  | De eerste 5 regels weergeven                                |
| `tail -n 5`                |                                  | De laatste 5 regels weergeven                               |

**Oefening: fruit**

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
3. Tel hoeveel het woord appel voorkomt.
5. Toon het fruit gesorteerd.
6. Sla het gesorteerde fruit op in fruit-gesorteerd.txt.
7. Verwijder dubbele opeenvolgende regels en sla het op in fruit-zonder-dubbels.txt.

# `|` doorsturen met Pipe

Met het pipe-command (`|`) stuur je de uitvoer van het ene commando rechtstreeks door naar het volgende commando.  
Je kunt een pipe lezen als **"en geef het resultaat door aan"**.

Bijvoorbeelden:

```
cat activiteiten.csv | sort
```
Hierbij wordt de inhoud van activiteiten.csv doorgegeven aan sort, dat de regels alfabetisch sorteert.

**Oefening: logboek**

1. Maak een een bestand activiteiten.txt met de volgende inhoud:
```
login
download
login
upload
login
download
logout
login
upload
logout
```
2. Bepaal hoeveel verschillende activiteiten er zijn.
3. Toon de eerste vier regels van het oorspronkelijke bestand.
4. Sla de eerste drie activiteiten uit de alfabetisch gesorteerde lijst op in het bestand eerste-activiteiten.txt.

# Oplossingen

{% capture oplossingen %}
Mijn eerste tekstbestand 
1. `printf "Maes\nBeroep: leerkracht\nCursus: meneermaes.be" > persoonlijk.txt`
2. `printf "\nIk leer werken met Bash" >> persoonlijk.txt`

Dagboek 
1. `date >> dagboek.txt`
2. `echo "Vandaag heb ik Bash geleerd" >> dagboek.txt`
3. `echo "$(date +%H:%M) Het is me gelukt om het tijdstip toe te voegen" >> dagboek.txt`

Mijn computer 
1. `ls > bestanden.txt`
2. `pwd > locatie.txt`
3. `date +%A > datum.txt`
4. `whoami > gebruiker.txt`
5. `du -ah . > groottes.txt`

Fruit 
1. `printf "appel\nbanaan\nappel\nkers\ndruif\nbanaan\nappel\nmango\nkers\nappel" > fruit.txt`
2. `grep "appel" fruit.txt`
3. `grep -c "appel" fruit.txt`
4. `sort fruit.txt`
5. `sort fruit.txt > fruit-gesorteerd.txt`
6. `uniq fruit-gesorteerd.txt fruit-zonder-dubbels.txt`

Logboek
1. `printf "login\ndownload\nlogin\nupload\nlogin\ndownload\nlogout\nlogin\nupload\nlogout" > activiteiten.txt` 
2. `sort activiteiten.txt | uniq`
3. `sort activiteiten.txt | uniq | wc -l`
4. `head -n 4 activiteiten.txt`
5. `sort activiteiten.txt | head -n 3 > eerste-activiteiten.txt`
{% endcapture %}

{% include toggle.html title="Oplossingen van de Oefeningen" content=oplossingen %}
