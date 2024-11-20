---
title: Zelf Aan De Slag Met Een Besturingssysteem
last_modified_at: 2024-11-14 09:07:20 +0200
date: 2024-10-23 15:39:25 +0200
---

> In dit hoofdstuk gaan we aan de slag met besturingssystemen die passen bij specifieke projecten.  

![](images/distros.gif)
<figcaption><a href="https://dribbble.com/shots/19045949-Distros-Only-Inside-a-Toolbox/attachments/14210303?mode=media">Jakub Steiner</a></figcaption>

# Hoe een nieuw OS installeren?

{% include toggle.html title="Dual Boot" content="
Dual boot is een configuratie waarbij **twee verschillende besturingssystemen op één computer** zijn geïnstalleerd, zodat je bij het opstarten kunt kiezen welk besturingssysteem je wilt gebruiken.

Het wordt vaak gebruikt om een nieuw besturingssysteem te **leren of testen**. Je kunt het nieuwe OS naast je bestaande systeem installeren en gebruiken om ermee vertrouwd te raken. Als je tevreden bent met het nieuwe besturingssysteem, kun je ervoor kiezen om het oude OS van de computer te verwijderen en alleen het nieuwe te behouden. Zo heb je de flexibiliteit om een nieuwe omgeving uit te proberen zonder meteen je huidige systeem op te geven.

**Voordelen**{: .goodText }
- Volledige toegang tot hardware
- Optimale performance
- Beste van twee werelden

**Nadelen**{: .badText }
- Complexe setup
- Moet steeds herstarten wanneer je van OS wil veranderen
- Elk OS heeft zijn eigen deel van de de harde schijf
" %}

{% include toggle.html title="Live USB" content="
Je installeert het OS op een USB-stick, en start het OS op vanaf deze USB-stick. Je gebruikt de hardware van de computer, maar het OS dat op de USB-stick staan.

Om een OS op een computer te installeren, werk je meestal met een live USB. Deze geeft je de optie om het besturingssysteem eerst te testen zonder iets aan je huidige installatie te veranderen en vervolgens het OS te installeren als je tevreden bent.

Er zijn **2 soorten** Live USB-sticks:
- **Tijdelijke opslag:** nieuwe data verdwijnt zodra je de computer uitzet.
- **Persistent opslag:** sommige Live USB's kun je configureren met een 'persistent storage', dit reserveert een deel van de USB-stick voor permanente opslag. Hiermee kun je veranderingen en bestanden bewaren, zelfs na herstart

**Voordelen**{: .goodText }
- Geen wijzigingen aan de computers
- Draagbaar systeem: eens geïnstalleerd op de USB-stick werkt het op alle computers
- Ideaal voor testen en reparatie
- Meestal heb je de optie om het OS te installeren op je computer na het eerst te kunnen testen

**Nadelen**{: .badText }
- Langzamer dan geïnstalleerd systeem
- Geen of beperkte opslagruimte
" %}

{% include toggle.html title="Virtuele Machine (VM)" content="
Een applicatie dat je kan installeren op je computer, die een computer simuleert.  
Het bekendste voorbeeld hier van is **VirtualBox**.

**Voordelen**{: .goodText }
- Veilig experimenteren zonder risico voor hoofdsysteem
- Meerdere OS'en tegelijk kunnen draaien
- **Ideaal voor testen en leren**

**Nadelen**{: .badText }
- Minder goede performance dan native installatie
- Beperkte toegang tot hardware
" %}

# Opdracht: Linux-distributie installatie

## Doelstelling

In deze opdracht gaan jullie aan de slag met het kiezen en installeren van een Linux-distributie die past bij een specifiek gebruik of doel.

{% include callout.html type="Projectverslag" content="
Creëer een **projectverslag** waarin je al je onderzoek, analyses en conclusies **overzichtelijk** vastlegt.  
Zorg ervoor dat het verslag zowel de stappen van je proces als de uiteindelijke resultaten duidelijk weergeeft.
" %}

## 1. Kies een scenario

Kies één van de volgende doelen waarvoor je Linux-distributie moet dienen, of bedenk er zelf een:
- Gaming
- Cybersecurity & ethical hacking
- Programming & developing
- Customizability (aanpasbaarheid)
- Creativity: Graphic design, video & music production

**Voeg het doel toe aan je projectverslag**.  
Bedenk **2 zaken die je wil doen of bereiken** met je gekozen Linux-distributie, en voeg deze toe aan je projectverslag.

## 2. Onderzoek

1. Zoek Linux-distributies op die passen bij je gekozen scenario.
2. Voeg een vergelijkingstabel toe aan je projectverslagt waarin je 2 Linux-distributies vergelijkt met criteria zoals:
	- Systeemvereisten
	- Gebruiksgemak
	- **Voeg extra criteria op die passen bij je gekozen scenario**
3. Kies een Linux-distributie en beschrijf waarom je deze gekozen hebt boven de andere.

## 3. installatie

Installeer de gekozen distributie in een virtuele machine door gebruik te maken van de software [VirtualBox](https://www.virtualbox.org)

{% include callout.html type="info" content="
VirtualBox is een krachtige, gratis en **open-source virtualisatie software**. Het stelt gebruikers in staat om virtuele computers, ook wel **virtuele machines (VM's)** genoemd, te creëren en te beheren op een gewone desktop of laptop computer.
" %}

{% include toggle.html title="Wat is een Virtuele Machine?" content="
Een virtuele machine is een soort **'computer in een computer'**. Het is een programma dat zich gedraagt als een aparte computer binnen je echte computer. **Je kunt er een besturingssysteem op installeren**, zoals Windows of Linux, zonder dat je je echte computer hoeft aan te passen. Alle onderdelen zoals opslag en geheugen worden virtueel nagebootst, maar ze gebruiken wel de echte hardware van je computer.
" %}

## 4. Voer je doel uit

Voer je twee specifieke taken uit.

Wanneer dit gelukt is laat je dit zien aan de leerkracht en documenteer je dit in je projectverslag.

## 5. Reflectie

Voeg de antwoorden op volgende vragen toe aan je projectverslagt:
1. Welke **licentie** heeft je gekozen Linux-distributie.  
	Voorzie een **screenshot** van waar je deze informatie gevonden hebt.
2. Schrijf in je **eigen woorden** wat deze licentie betekend, wat mag wel, wat mag je niet en wat moet je...
3. Wat zijn **voordelen en nadelen** van het gebruik van een OS onder deze licentie?
4. Beschrijf hoe Linux bijdraagt aan 2 van de volgende zaken:
	- Samenhorigheid
	- Privacy
	- Duurzaamheid
	- Ongelijkheid verminderen
	- Digitale geletterdheid

## Puntenverdeling

{% include punten.html data='zelf-aan-de-slag-met-een-besturingssysteem-punten' %}
{% include doelen.html data='Zelf-aan-de-slag-met-een-besturingssysteem-doelen' %}
