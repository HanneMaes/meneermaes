---
title: WSL
last_modified_at: 2025-04-22 14:01:24 +0200
date: 2025-04-22 13:28:45 +0200
---

> WSL staat voor **Windows Subsystem for Linux**

# Wat is WSL?

WSL is een manier om **Linux op Windows** te draaien, zonder dat je een virtuele machine hoeft te gebruiken of je computer hoeft te dual-booten.  
Met WSL kun je gewoon in Windows blijven werken, maar toch gebruik maken van een echte Linux-omgeving, rechtstreeks vanuit je **terminal**.

**Verschillende versies:**  
- **WSL 2** draait een echte Linux-kernel in een lichte virtuele machine (met Hyper-V technologie). Veel sneller en beter compatibel.  
- **WSL 1** daarentegen werkt meer als een tolk: het vertaalt Linux-commando’s naar Windows-opdrachten, wat handig is maar minder krachtig en soms niet volledig compatibel met alle Linux-tools.

**Vandaag gebruiken we WSL 2**, die is stabieler, sneller en krachtiger.

In 2016 was het groot nieuws dat **Microsoft samenwerkte met Canonical** (van Ubuntu). Vroeger waren Microsoft en Linux **bittere rivalen**. Nu draaien ze hand in hand!

# Waarom zou je WSL gebruiken als IT’er?

- Je kan dezelfde krachtige tools gebruiken zoals op een echte Linux-server.
- De meeste servers waarop websites, apps of backend-diensten draaien, gebruiken Linux. Je kan applicaties lokaal bouwen én testen alsof ze op een echte Linux-server draaien.
- Je kan leren werken met Linux zonder een aparte pc of dual-boot.

# Hoe installeer je WSL

**Voorwaarden:**
- Windows 10 versie 2004 of hoger (build 19041)

**Installatie:**
1. Ga naar de **Microsoft Store** en installeer **Ubuntu**, of een van de andere ondersteunde Linux-distributies.
2. Open Ubuntu WSL via het **Start-menu**.

**Testen of het werkt:**
1. Open een terminal (Windows Terminal of "Ubuntu" via Start).
2. Typ: `uname -a`.  
   Uname staat voor "Unix Name" en toont **systeeminformatie**, de -a vlag betekent "all", dus: toon alle beschikbare info.
3. Je zou iets moeten zien als: `Linux DESKTOP-1234 5.15.90.1-microsoft-standard-WSL2 ...`.

# WSL tips

- Je kunt `code .` gebruiken om **Visual Studio Code** te openen in je huidige Linux-map. Zorg wel dat de **extensie “Remote - WSL”** geïnstalleerd is in VS Code.
- Linux-bestanden staan in Windows onder: {% include filePath.html fileOrPath='\\wsl$\Ubuntu\home\jouwgebruikersnaam' %} 
- En omgekeerd kun je je Windows-schijf vinden vanuit Linux via: {% include filePath.html fileOrPath='/mnt/c/Users/...' %} 
