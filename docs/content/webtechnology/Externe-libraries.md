---
title: Externe libraries
date: 2024-04-23 13:06:08 +0200
---

JavaScript- en CSS-libraries zijn verzamelingen van **voorgeprogrammeerde functies en stijlen** die kunnen worden gebruikt om de **ontwikkeling** van webpagina's te **versnellen en verbeteren**.

# Voorbeeld: AOS.js *(library)*

**Animate on scroll (AOS.js)** is een **library** die je toelaat elementen met een animatie in beeld te laten komen.

{% include browser.html img='images/aos-voorbeeld.gif' width='500px' %}

## Oefening: voeg AOS.js toe aan je portfolio website

1. Surf naar: [https://michalsnik.github.io/aos/](https://michalsnik.github.io/aos/),
2. Download en unzip de code.
3. Plaats de bestanden in {% include filePath.html fileOrPath='aos-master/dist/' %} in de map van je website, in een folder genaamd {% include filePath.html fileOrPath='libraries/' %}. Dit is de code van de library.  
	![](images/lib-folder.png){: width="500" }
4. Link in {% include filePath.html fileOrPath='index.html' %} naar de **CSS** en **JS** bestanden van de library.  
	Ondertussen zou je al moeten weten waar deze zijn code in je HTML-bestand moeten komen.
	```html
	<link rel="stylesheet" href="libraries/aos.css">
	<script src="libraries/aos.js"></script>
	```
5. Voeg deze code toe om de `AOS.js` library te starten. Dit moet onder de code staan die `aos.js` inlaad omdat de library eerst ingeladen moet zijn alvorens we de functies ervan kunnen gebruiken.
	```html
	<script>
		AOS.init();
	</script>
	```
6. Voeg de code voor het effect dat je wil toe aan een HTML-tag.
	```html
	<h1 data-aos="fade-down">Header text</h1>
	```

{% include callout.html type='uitdaging' content='Zoek uit hoe je animaties later kan starten en kan bepalen hoe lang ze duren.' %}

# Populaire libraries

Hieronder staan een aantal veelgebruikte libraries:
- [Hover animaties](http://ianlunn.github.io/Hover/)
- [Hover & loading animatie](https://www.csswand.dev/)
- [Reveal animaties](https://www.minimamente.com/project/magic/)
- [Loading animatie](https://nzbin.github.io/three-dots/)
- [Animate on scroll (AOS.JS)](https://michalsnik.github.io/aos/)
- [Hamburger menu's](https://jonsuh.com/hamburgers/)
- [Patterns](https://bansal.io/)
- [Interactieve 3D content](https://threejs.org/)

# Librarie vs framework

- Een **library** biedt een set tools en functies die je kan gebruiken om *(meestal kleine)* **specifieke taken** uit te voeren.
- Een **framework** bied een een omvattende **structuur en werkwijze** die je **moet** volgen, inclusief richtlijnen en conventies.

{% include callout.html type='info' content='Een library kan je best kiezen bij de start van grote projecten. Terwijl je een library later kan toevoegen wanneer je nood hebt aan specifieke functionaliteit.' %}

# Design systems *(framework)*

Een design system in is een **verzameling** van herbruikbare **code en elementen** die je kan gebruiken bij het maken van een project. Het bevat onder andere zaken als knoppen, navigatiebalken, icoontjes, kleuren, ...  
Door een design system te gebruiken kan je snel een websites maken met een mooi en bruikbaar ontwerpen zonder alles handmatig te moeten ontwerpen.

Hieronder een aantal veelgebruikte design systems:
- [Simple.css](https://simplecss.org/)
- [Google Material Design System](https://materializecss.com/)

# Opdracht libraries

1. Maak een website met een **design system** naar keuze, start met de homepage waarin staat welk **design system** je gekozen hebt en **waarom**. 
2. Maak een pagina met afbeeldingen en gebruik een **lightbox library** *(ontdek zelf wat een lightbox is)*.
3. Maak minstens **2** andere pagina's die elk een **library** gebruiken.  
	Minstens 1 library moet je zelf zoeken en mag niet in de cursus staan. *(AOS.js telt niet als library die in de cursus staat, het is de bedoeling dat je zelf leert uitzoeken hoe je libraries kan gebruiken.)*  
	Op elke pagina vermeld je:
- **Welke** library het is en **wat** ze doet.
- Hoe je deze library kan gebruiken, met **code voorbeelden** (een kleine tutorial).

{% include callout.html type='tip' content='Om code weer te geven op een HTML-pagina zonder dat deze wordt uitgevoerd, kan je de [Highlight.js](https://highlightjs.org/) library gebruiken.' %}

{% include punten.html data='Externe-libraries' %}

# Local files vs hosted files

Library files *(.css, .js)* kunnen lokaal worden gehost, waarbij de bestanden rechtstreeks in de folder van het project worden geplaatst, of extern worden gehost, waarbij de bestanden worden geladen vanaf een externe locatie. 

```html
<link rel="stylesheet" href="<script src="libraries/aos.js"></script>">
```
```html
<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
```

## Hostel files

Gehoste bestanden staan op **externe servers**, meestal van derden zoals Content Delivery Networks (CDN's).

**Voordelen**{: .goodText } van hostel files:

- **Snellere laadtijden**{: .goodText }: als het wordt gehost op een goed geoptimaliseerde server. Gehoste bestanden worden vaak geleverd via Content Delivery Networks (CDN's), wat betekent dat ze mogelijk al in de cache van de gebruiker staan of worden geleverd vanuit een server die dichter bij de gebruiker staat.
- **Geen onderhoud**{: .goodText }: Je hoeft geen lokale kopieën van de bestanden te onderhouden of te updaten. Wanneer er een nieuwe versie beschikbaar is, wordt deze automatisch via de CDN geleverd.

## Local files

Lokale bestanden bevinden zich op je eigen server *(of computer)*.

**Voordelen**{: .goodText } van local files:

- **Controle**{: .goodText }: Wanneer een bestand aangepast word op een externe server, kan het de werking van je website verstoren, zonder dat jij dat weet. Bij lokale bestand weet je dat het bestand niet aangepast zal worden en dus dat het zal blijven werken.
- **Geen afhankelijkheid van derden**{: .goodText }: Je bent niet afhankelijk van de externe serviceprovider *(zoals CDN)* om de bestanden beschikbaar te houden. Als deze een storing hebben, kan dit van invloed zijn op de beschikbaarheid van je website.
- **Privacy en beveiliging**{: .goodText }: Als je externe scripts of bibliotheken laadt, geef je controle uit handen over wat er op je website wordt geladen. Hoewel CDNs doorgaans betrouwbaar zijn, brengt het laden van externe bestanden altijd een zeker risico met zich mee.

## NPM *(Node package manager)*

![NPM logo](images/Npm-logo.svg){: .square }{: width='300px' }

Npm is een **package manager** voor JavaScript.  
Een package manager is een tool die wordt gebruikt voor het beheren van pakketten of verzamelingen van bestanden.  
Npm maakt het gemakkelijk om JavaScript-libraries te installeren en up-to-date te houden.