---
title: Bash Scripting
last_modified: 2026-01-08 14:34:31 +0100
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

Je bash script moet altijd beginnen met deze regel, zo weet je systeem dat het script met de Bash-shell moet worden uitgevoerd.

```bash
#!/bin/bash
# Je bash script moet altijd starten met deze code

# De rest van je code ...
```

## Variabelen

```bash
naam="Maes"
echo "Hallo, $naam"
```

## Invoer

```bash
echo "Wat is je naam?"
read gebruikersnaam
echo "Hallo, $gebruikersnaam! Welkom bij mijn Bash-script."
```

## If-statement

```bash
if [ $naam == "Maes" ]; then
  echo "Je bent de beste leerkracht!"
else
  echo "Wie ben jij?"
fi
```

## For Loop

```bash
for i in {1..5}
do
  echo "Nummer $i"
done
```

## While Loop

```bash
count=1
while [ $count -le 5 ]
do
  echo "Telling: $count"
  ((count++))
done
```

## Functies

```bash
functie_naam() {
  echo "Dit is een functie"
}
functie_naam
```

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
- Toont hoeveel ruimte de huidige map in beslag neemt met het `du -hs` command. Toon niet enkel het getal maar zet het in een zin zodat het duidelijk is wat de betekenis is.

**Stap 2: Backups maken**

Maak een **functie** die een backup maakt van een map. Deze functie krijgt **2 argumenten**:
- De naam van de map die geback-upt moet worden
- De naam van de backup-map

Voeg de datum van de backup toe aan het einde van de bestandsnaam.

**Stap 3: Menu**

Gebruik een **while-loop** om een menu te tonen dat blijft herhalen.  
Het menu bevat minstens:
- Backup maken van een map
- Oude bestanden opruimen
- Stoppen

Zolang de gebruiker niet kiest om te stoppen, blijft het script zich herhalen.

**Stap 4: Opruimen van oude bestanden**

Vraag aan de gebruiker:
- Een map
- Het aantal dagen

Verwijder bestanden die ouder zijn dan het opgegeven aantal dagen.

**Voorbeeld**: stel dat je alle bestanden ouder dan 7 dagen uit een map ~/testmap wilt verwijderen:
```sh 
# TOON bestanden ouder dan 7 dagen
find ~/testmap -type f -mtime +7 
  # find: zoekt bestanden/mappen
  # ~/testmap: de map waarin gezocht wordt
  # -type f: alleen gewone bestanden (geen mappen)
  # -mtime +7: bestanden die meer dan 7 dagen oud zijn
  # -delete:  verwijdert de gevonden bestanden

# VERWIJDER bestanden ouder dan 7 dagen
find ~/testmap -type f -mtime +7 -delete
```

Als dit gedaan is toon je:
- Hoeveel ruimte de map in beslag nam voor de opkuis
- Hoeveel bestanden zijn verwijderd.
- Hoeveel ruimte de map nu in beslag neemt.
- Hoeveel percent kleiner de map geworden is.
