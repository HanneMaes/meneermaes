---
title: Bash Scripting
last_modified: 2026-01-07 09:01:17 +0100
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

# Opdracht: Je 1e Bash script

**Aanmaak**
1. Maak een nieuw bash script aan.
2. Zoek uit hoe je het script **executable** kan maken zodat je het kan uitvoeren.
3. Zoek uit hoe je het script uit kan voeren en voer het uit.

**Code**
1. Laat het script vragen naar de naam van de website.
2. Maak een folder aan met de naam van de website
3. Maak in deze folder de volgende bestanden en subfolders aan:
  - index.html
  - style.css 
  - script.js 
  - images/
  - blogposts/
4. Laat een bericht zien dat de bestanden en folders aangemaakt zijn en toon ze ook.
5. Vraag hoeveel blogposts de gebruiker wil hebben en maak dit aantal .html bestanden aan in de folder blogposts/
  - post-1.html
  - post-2.html 
  - ...
6. Pas je script aan zodat de bestanden niet meer leeg aangemaakt worden.
  - .html bestanden bevatten de correct startcode en laden style.css in.
  - style.css geeft de achtergrond en h1-titels een kleur.
