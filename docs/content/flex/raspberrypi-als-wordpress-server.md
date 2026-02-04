---
title: Raspberry Pi als Wordpress Server
created: 2026-01-27T15:28:48+01:00
---

# Wat is Wordpress

![Wordpress logo](images/wordpress.png)

WordPress is een open-source **contentmanagementsysteem (CMS)** waarmee je websites kan bouwen en beheren zonder alles van nul te moeten programmeren.

Vandaag draait ongeveer **40% van alle websites wereldwijd** op WordPress.  
Dat maakt het veruit het meest gebruikte CMS ter wereld. Van kleine hobbyprojecten tot professionele platforms.

## Wat is een CMS

Een CMS (Content Management System) is software waarmee je een **website kan beheren** zonder dat je elke pagina handmatig moet programmeren.

Via een CMS heb je een website waarbij jij, of de persoon of het bedrijf waarvoor je de website maakt, **de inhoud kan beheren via een UI**, in plaats van HTML-bestanden te moeten schrijven en uploaden.

## Voordelen van WordPress

- Open-source en gratis
- Grote community van ontwikkelaars:  
  *Duizenden thema’s en plugins*
- Veel documentatie en ondersteuning online
- Relevant op de arbeidsmarkt:  
  *WordPress wordt massaal gebruikt in de praktijk*  
  *Kennis ervan is een concrete meerwaarde voor webdevelopers*  
  *Veel freelance en professionele opdrachten draaien rond WordPress*

## Nadelen van WordPress

- WordPress websites zijn groter:  
  *Het gebruikt een databse*  
  *Het voert PHP-code uit op elke pagina*  
- Veiligheid vraagt aandacht:  
  *Populair doelwit voor aanvallen*
  *Slechte plugins of verouderde installaties vormen risico’s*
- Prestatieproblemen:  
  *Te veel plugins kunnen een site traag maken*  
  *Thema’s zijn vaak zwaar en inefficiënt*  

> WordPress is een **algemene oplossing**, geen wondermiddel

## Illusie van “geen code nodig”

Veel gebruikers denken dat WordPress codevrij is, maar in de realiteit blijft kennis van HTML, CSS, PHP en SQL belangrijk.

## Waarom WordPress hosten op je eigen Raspberry Pi

Een Raspberry Pi gebruiken als Wordpress server heeft grote educatieve waarde:
- Volledige controle.  
  *Je beheert zelf het besturingssysteem, de webserver, de database en WordPress. Niets is verborgen.*
- Digitale autonomie:
  *Je bent niet afhankelijk van grote platformen of cloudproviders. Je begrijpt waar je data staat en hoe die wordt beheerd.*
- Geen hosting geheimen meer:
  *Je leert wat hosting écht betekent: configuratie, beveiliging, updates en foutopsporing.*
- Kosten en duurzaamheid:
  *Een Raspberry Pi is goedkoop, energiezuinig en perfect voor experimenten en leren.*

## WordPress.org vs WordPress.com

**WordPress.org**
- De **open-source** software die je zelf downloadt en installeert
- Volledige vrijheid: eigen hosting, thema’s, plugins en code
- Jij bent verantwoordelijk voor onderhoud en beveiliging
- Dit is wat professionele developers gebruiken

**WordPress.com**
- Een commerciële dienst die WordPress voor jou host
- Beperkte vrijheid, zeker in de gratis en goedkope formules
- Minder controle over code, plugins en data

# Opdracht: Raspberry Pi als WordPress server

Je krijgt **geen stappenplan**. In plaats daarvan ga je zelf op zoek naar informatie, probeer je oplossingen uit en reflecteer je regelmatig over je leerproces.

Het einddoel is tweeledig:
- **Product**: een werkende WordPress-installatie op je Raspberry Pi
- **Proces**: aantonen dat je doelgericht onderzocht, kritisch informatie verwerkte en je leerproces kon bijsturen, in een **duidelijk, gestructureerd en professioneel digitaal document**

## Zoekstrategie en bronkritiek

Voor je begint, bepaal je hoe je informatie zal zoeken.  
Noteer alles duidelijk in het document.

Noteer:
1. In welke taal ga ik zoeken?
2. Welke soorten bronnen verwacht ik te gebruiken?

Noteer bij het maken van je onderzoek:
1. Welke zoektermen ga ik gebruiken?
2. Kies minstens **2 verschillende** bronnen.
3. Welke bron vertrouw ik het meest? Waarom?

Je kan AI-tools gebruiken als ondersteuning, maar **AI is geen bron**.  
Je mag AI gebruiken om:
- Je vraag beter te formuleren
- Vaktermen te laten uitleggen in eenvoudigere taal
- Mogelijke zoektermen of invalshoeken te bedenken

Je mag AI niet gebruiken als:
- Eindantwoord dat je zomaar overneemt
- Vervanging van echte bronnen

## Technisch vooronderzoek

Onderzoeksvragen:
1. Welk **besturingssysteem** draait meestal op een Raspberry Pi?
2. Wat is de **functie van een webserver**?
3. Waarom heeft WordPress een **database** nodig?
4. Wat is de rol van **PHP** binnen WordPress?
5. Maak een eenvoudig **schema** dat toont hoe deze onderdelen samenwerken.
6. Wat zijn **VNC**, **SSH** en **Raspberry Pi Connect**? Geef minstens 1 voordeel van elke technologie.

Reflectie:
1. Welke begrippen waren **nieuw** voor mij?
2. **Hoe** heb ik geprobeerd ze te begrijpen (lezen, video, schema, uitleg vragen)?

## Installatie OS

Voor je begint te installeren, voeg je een **logboek** toe aan het document. Dit logboek gebruik je tijdens de **hele opdracht**.

> Een logboek is geen stappenplan achteraf, maar een verslag tijdens het werken.

Het logboek toont hoe je denkt en leert, niet alleen wat er lukt.
Tijdens deze opdracht is het **niet erg om fouten te maken**. Integendeel: **fouten zijn vaak leerrijker** dan wanneer alles meteen lukt. Wanneer iets niet werkt, documenteer dit dan zorgvuldig:
- Welke foutmelding of probleem je tegenkwam.
- Welke stappen je hebt ondernomen om het probleem op te lossen.

Nu ga je **praktisch** aan de slag met het installeren van een besturingssysteem (OS) op een Raspberry Pi.

Je werkt onderzoekend:
- Je volgt geen blind stappenplan
- Je probeert te begrijpen wat elke stap doet.
- Je staat stil bij keuzes die je maakt.

**Stappen:**
1. Schrijf in je logboek welk OS heb ik gekozen en **waarom**?  
2. Voeg **screenshots** toe om te documenteren hoe je het OS hebt kunnen installeren.

**Reflectie:**
- Wat ging vlot? Waarom?
- Waar liep ik vast?
- Welke strategie gebruikte ik?
- Wat zou ik volgende keer anders aanpakken?

## Installatie WordPress 

Nu de Raspberry Pi een OS heeft, is het tijd om **WordPress te installeren**:
1. Zoek doelgericht naar bronnen die je kunnen helpen bij de installatie.
2. Beoordeel deze bronnen kritisch en kies er één waarmee je aan de slag gaat.
  - Merk je tijdens de installatie dat een andere bron toch geschikter is, dan mag je van bron veranderen. Dit maakt deel uit van een realistisch leerproces.

Documenteer het **volledige verloop** duidelijk in je logboek, inclusief gemaakte keuzes, ondernomen stappen en screenshots ter ondersteuning.

**Reflectie:**
- Wat zou ik anders aanpakken als ik opnieuw moest beginnen?
- Wat heb ik geleerd dat ook nuttig is voor andere IT-opdrachten?

## Puntenverdeling

{% include punten.html data='raspberry-pi-als-wordpress-server' %}









