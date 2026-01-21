---
title: Bash Scripting
last_modified: 2026-01-21 17:22:10 +0100
created: 2025-01-15 15:21:22 +0200
---

# Wat is Bash?

Het is de taal waarmee je **Linux** & **MacOS** kunt **besturen via de terminal**. In plaats van alles met je muis te doen, kun je met Bash direct commando’s invoeren om het systeem te bedienen. Het maakt het mogelijk om snel dingen te doen die je normaal met een grafische interface zou doen, zoals bestanden kopiëren, programma’s starten, of instellingen aanpassen.

Wat Bash echt krachtig maakt, is dat je er ook mee kunt programmeren. Dit betekent dat je taken die je normaal handmatig zou uitvoeren (zoals een reeks commando's achter elkaar uitvoeren) kunt **automatiseren met een Bash-script**. Hierdoor kun je dingen sneller, efficiënter of automatisch doen, zonder steeds weer hetzelfde handmatige werk te herhalen.

**Bijvoorbeeld:**

- Automatisch regelmatig back-ups maken van belangrijke bestanden of mappen.
- Automatisch je systeem en softwarepakketten up-to-date houden.
- Je kunt Bash gebruiken om meldingen naar jezelf of anderen te sturen wanneer bepaalde gebeurtenissen plaatsvinden

## Bash op servers

**Linux is het meestgebruikte besturingssysteem voor servers wereldwijd**. Het wordt vaak gekozen vanwege zijn stabiliteit, veiligheid, en open-source karakter. Omdat de meeste Linux-servers geen grafische gebruikersinterface (GUI) hebben, wordt **alles via de terminal beheerd**, wat betekent dat kennis van de Bash-shell cruciaal is voor serverbeheer.

**Bijvoorbeeld:**

- Wanneer je werkt met meerdere servers, kan het bijwerken van het systeem op elke server een tijdrovende taak zijn. Met Bash kun je updates automatisch uitvoeren op al je servers.
- Met Bash kun je de gezondheid van je server controleren, zoals het controleren van de schijfruimte of het geheugen, en meldingen sturen als er een probleem is.
- Het regelmatig maken van back-ups van je serverbestanden en databases is cruciaal. Met Bash kun je back-upscripts schrijven die dit automatisch doen, bijvoorbeeld door dagelijkse back-ups van je serverbestanden en MySQL-databases te maken.
- Op een server wil je ervoor zorgen dat kritieke services, zoals een webserver of database, altijd actief blijven. Met Bash kun je automatisch controleren of deze services draaien en ze opnieuw starten als dat niet het geval is.

# Linux of Git Bash

Tijdens deze opdracht zullen we werken met Bash, de shell waarmee je commando’s invoert in een Linux-omgeving.
Je kan op 2 manieren met Bash werken:

- **Git Bash**  
   Git Bash is een programma waarmee je op een Windows-computer Linux-achtige commando’s kunt gebruiken. Het geeft je toegang tot de Bash-shell, die normaal gesproken op Linux en macOS wordt gebruikt.
- **Een volledige Linux-versie in een virtuele machine**  
  Dit geeft je de complete Linux-ervaring.

Je mag zelf kiezen welke optie je gebruikt om met Bash aan de slag te gaan.

# Bash scripts aanmaken en uitvoeren

1. Open de terminal
   - In de meeste Linux-distributies kun je de terminal openen door op {% include btn.html btn='Ctrl' %} {% include btn.html btn='Alt' %} {% include btn.html btn='T' %}
   - Of je kunt zoeken naar **"Terminal"** in het applicatiemenu.
2. Kijken op welke locatie je zit: `pwd`
3. Kijken welke bestanden er op deze locatie staan: `ls`
4. Nieuwe bestanden aanmaken:
   - `touch bestand.txt`
   - `touch script.sh`

# Bash syntax

## De Bang Start Code

Je bash script moet **altijd** beginnen met deze regel.  
Zo weet het systeem dat het script met de Bash-shell moet worden uitgevoerd.

```bash
#!/usr/bin/env bash
# Je bash script moet altijd starten met deze code

# De rest van je code ...
```

## Variabelen

```bash
naam="Maes"
echo "Hallo, $naam"
```

| Syntax        | Betekenis           | Opmerking                 |
|---------------|---------------------|---------------------------|
| `naam="Maes"` | variabele instellen | **geen spaties** rond `=` |
| `leeftijd=18` | numerieke variabele | bash kent geen types      |
| `$naam`       | waarde gebruiken    | altijd met `$`            |

**Veelgemaakte fouten**
- Fout: `naam = "Maes"` (spaties maken er een command van)
- Fout: `$naam="Maes"`
- Juist: `naam="Maes"`

## Invoer

```bash
echo "Wat is je naam?"
read gebruikersnaam
echo "Hallo, $gebruikersnaam! Welkom bij mijn Bash-script."
```

| Syntax                  | Betekenis                         | Staat voor |
|-------------------------|-----------------------------------|------------|
| `read -p "Naam: " naam` | invoer vragen                     | p = prompt |
| `read -s wachtwoord`    | verborgen invoer                  | s = silent |
| `read -r tekst`         | geen escape-interpretatie bij `\` | r = raw    |

## If-statement *(modern Bash)*

```bash
naam="Maes"

if [[ $naam == "Maes" ]]; then
  echo "Je bent de beste leerkracht!"
else
  echo "Wie ben jij?"
fi
```

### Getallen

| Operator | Betekenis             | Staat voor            |
|----------|-----------------------|-----------------------|
| `-eq`    | gelijk aan            | equal                 |
| `-ne`    | niet gelijk aan       | not equal             |
| `-lt`    | kleiner dan           | less than             |
| `-le`    | kleiner of gelijk aan | less than or equal    |
| `-gt`    | groter dan            | greater than          |
| `-ge`    | groter of gelijk aan  | greater than or equal |

### Strings

| Operator   | Betekenis   |
| ---------- | ----------- |
| `$a == $b` | Gelijk aan  |
| `-z $a`    | Leeg        |
| `-n $a`    | Niet leeg   |

## Wiskundige berekeningen

Wiskundige berekeningen zet je tussen `(( ... ))`.

**Waarom?**
- Bash behandelt alles standaard als tekst.
- `(( ... ))` vertelt Bash: **dit is rekenwerk**.

```bash
a=4 
b=7

# Zonder (( )): tekst
echo $a + $b # Output: 4 + 7

# Met (( )): rekenen
echo $(( $a + $b )) # Output: 11
```

**Waarom is `$` nodig in `echo $(( $a + $b ))`?**
- `$(( ... ))` is geen “variabele”  
  `(( ... ))` is een rekenconstructie, geen variabele.  
  Je zet er een rekensom in, en Bash geeft het resultaat terug.
- `$a` en `$b` zijn variabelen  
  Om de waarde van een variabele te gebruiken, moet je `$` ervoor zetten:
  - `a` = de naam van de variabele
  - `$a` = de waarde van de variabele

```bash
a=4

echo a    # geeft: a
echo $a   # geeft: 4

# Dus in de som:
$(( $a + $b ))
```

**Betekent:**
- Neem de waarde van a (`$a`)
- Neem de waarde van b (`$b`)
- Tel ze op
- Geef het resultaat terug


| Schrijfwijze     | Betekenis                 |
| ---------------- | -----------------------   |
| `a`              | De string "a"             |
| `$a`             | Waarde van de variabele a |
| `$(( $a + $b ))` | Tel de waarden op     |

## For Loop

```bash
for ((i=1; i<=5; i++)); do
  echo "Nummer $i"
done
```

| Vorm                | Betekenis   | Wanneer gebruiken                               |
|---------------------|-------------|-------------------------------------------------|
| `for i in 1 2 3`    | vaste lijst | eenvoudige herhaling                            |
| `for i in {1..5}`   | bereik      | tellen                                          |
| `for file in *.txt` | bestanden   | alle bestanden die eindigen op .txt in deze map |

## While Loop *(modern Bash)*

```bash
count=1
while (( count <= 5 )); do
  echo "Telling: $count"
  ((count++))
done
```

## Functies

### Basis functie

```bash
functie_naam() {
  echo "Dit is een functie"
}

functie_naam
```

### Functie met parameters

```bash
groet() {
  echo "Hallo $1"
}

groet Maes
```

| Syntax          | Betekenis           | Opmerking          |
|-----------------|---------------------|--------------------|
| `functie() { }` | functie definiëren  | standaard          |
| `functie`       | functie oproepen    | zonder ()          |
| `echo "tekst"`  | waarde “teruggeven” | via output         |
| `$1, $2`        | parameters          | positie-argumenten |

# Opdracht 1: Automatisatie nieuw project

Je maakt vaak websites en moet telkens opnieuw dezelfde mappen aanmaken. **Dat kost tijd.** Daarom schrijf je een Bash-script dat dit werk automatisch voor jou doet.

**Stap 1: Voorbereiding**

1. Maak een nieuw Bash-script aan.
2. Voeg de correcte shebang toe bovenaan `(#!/bin/bash)`.
3. Maak het script executable zodat je het kan uitvoeren `chmod +x scriptnaam.sh`.
4. Voer het script uit om te testen `bash scriptnaam.sh`.

**Stap 2: Projectinformatie**

1. Laat het script de gebruiker vragen naar de naam van de website.
2. Maak een map aan met de naam van de website.

**Stap 3: Basisbestanden en mappen**

1. Maak in deze map de volgende bestanden en submappen aan:
  - {% include filePath.html fileOrPath='index.html' %} 
  - {% include filePath.html fileOrPath='style.css' %}
  - {% include filePath.html fileOrPath='script.js' %}
  - {% include filePath.html fileOrPath='images/' %} 
  - {% include filePath.html fileOrPath='blogposts/' %}
2. Laat een bericht zien dat de bestanden en mappen aangemaakt zijn.  
  Toon de structuur van de mappen in een boomstructuur via `tree`.

**Stap 4: Blogposts genereren**

1. Vraag hoeveel blogposts de gebruiker wil hebben.
2. Maak dit aantal {% include filePath.html fileOrPath='.html' %} bestanden aan in de map {% include filePath.html fileOrPath='blogposts/' %}:
  - {% include filePath.html fileOrPath='post-1.html' %}
  - {% include filePath.html fileOrPath='post-2.html' %}
  - {% include filePath.html fileOrPath='etc...' %}

**Stap 5: Dynamische inhoud**

1. Pas het script aan zodat de bestanden niet meer leeg zijn:
2. De {% include filePath.html fileOrPath='.html' %} bestanden bevatten de correcte startcode `<!DOCTYPE html>`, `<html>`, ...
3. De bestanden laden automatisch {% include filePath.html fileOrPath='style.css' %} in.
4. Pas {% include filePath.html fileOrPath='style.css' %} aan zodat de gebruiker zelf de achtergrondkleur en kleur van de `<h1>` kan kiezen. Je vraagt in je script naar deze kleuren.
5. Toon de inhoud van {% include filePath.html fileOrPath='style.css' %} zodat je kan controleren of de juiste kleuren gebruikt zijn.

**Stap 6: Dynamische titels en koppen**

1. Geef alle {% include filePath.html fileOrPath='.html' %} bestanden een dynamische `title` en `<h1>` hoofding:
  - {% include filePath.html fileOrPath='index.html' %}: de naam van de website
  - {% include filePath.html fileOrPath='post-1.html' %}: Post 1
  - {% include filePath.html fileOrPath='post-2.html' %}: Post 2
  - {% include filePath.html fileOrPath='etc...' %}

# Opdracht 2: Backup- & opruimscript

Je gebruikt een Raspberry Pi als kleine server. Na een tijdje staan er veel bestanden in je home-folder: oude logs, testbestanden, tijdelijke bestanden, ...

Om overzicht te houden wil je met één script:
- Belangrijke mappen back-uppen
- Oude bestanden opruimen
- Dit meerdere keren kunnen uitvoeren zonder alles opnieuw te typen

**Stap 1: Systeeminformatie tonen**

Maak een script aan dat:
- Een welkombericht toont
- De huidige datum toont met het `date` of `$(date '+%H:%M:%S')` command
- De huidige map toont

**Stap 2: Grootte functie**

Schrijf een functie die:
- Eén argument krijgt: de naam van een map
- De grootte van deze map berekent met het `du -hs` command. 
- De functie **geeft deze grootte terug** zodat je ze later in je code kan gebruiken.
- Gebruik deze functie om de grootte te tonen van de huidige map, toon niet enkel het getal maar zet het in een zin zodat het duidelijk is wat de betekenis is.

**Stap 3: Backups maken**

1. Maak een **functie** die een backup maakt van een map. Deze functie krijgt **2 argumenten**:
  - De naam van de **map** die geback-upt moet worden
  - De naam van de **backup-map**
2. Voeg de datum van de backup toe aan het einde van de bestandsnaam.

**Stap 4: Menu**

Gebruik een **while-loop** om een menu te tonen dat blijft herhalen.  
Het menu bevat minstens:
- Backup maken van een map
- Oude bestanden opruimen
- Stoppen

Zolang de gebruiker niet kiest om te stoppen, blijft het script zich herhalen.

**Stap 5: Opruimen van oude bestanden**

1. Vraag aan de gebruiker:
  - Een map
  - Het aantal dagen
2. Toon alle bestanden in de map die ouders zijn dan het opgegeven aantal dagen met die command:
```sh 
# TOON bestanden ouder dan 7 dagen
find ~/testmap -type f -mtime +7 
  # find: zoekt bestanden/mappen
  # ~/testmap: de map waarin gezocht wordt
  # -type f: alleen gewone bestanden (geen mappen)
  # -mtime +7: bestanden die meer dan 7 dagen oud zijn
  # -delete:  verwijdert de gevonden bestanden
```
3. Vraag of het OK is deze bestanden te verwijderen en verwijder ze met die command:
```sh 
# VERWIJDER bestanden ouder dan 7 dagen
find ~/testmap -type f -mtime +7 -delete
```
4. Daarna toon je:
- Hoeveel ruimte de map in beslag nam *(door gebruik te maken van je eigen functie)* voor de opkuis
- Hoeveel bestanden zijn verwijderd.
- Hoeveel ruimte de map nu in beslag neemt *(door gebruik te maken van je eigen functie)*.
- Hoeveel percent kleiner de map geworden is.

## Uitbreiding

Gebruik **Rclone** om je backup-map up te loaden naar **Google Drive**.
