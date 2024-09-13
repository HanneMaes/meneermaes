---
title: Je 1e code
last_modified_at: 2024-05-03T07:12:37
date: Thu, Sep 12, 2024  20:47:23 PM
---

# Bestand extensies
## Wat zijn bestand extensies?

Bestand extensies zijn de letters die na het punt in een bestandsnaam komen.
**Ze geven aan wat voor type bestand het is** en helpen het besturingssysteem te bepalen welke applicatie het bestand kan openen. 
Ze fungeren als een soort label dat vertelt hoe het bestand gelezen of geopend moet worden.

- text**.txt**
- afbeeling**.jpg**
- word-document**.docx**

In webdesign gebruiken we verschillende soorten bestanden. Het is belangrijk om de bestandsextensies zichtbaar te hebben, omdat dit ons helpt te weten welk type bestand we gebruiken.
Helaas verbergt Windows deze extensies.

**Door de extensies zichtbaar te houden, kunnen we gemakkelijk bestanden identificeren en van extensie (en dus ook type) veranderen.**

## Bestand extensies tonen

{% include ui.html ui='beeld, opties, extensies voor bekende bestandstypes verbergen' %}

![Bestand extensies tonen](images/bestand-extensies-tonen.png)

## Experiment

1. **Download een afbeelding** van het internet.  
Door de **.jpg, .jpeg of .png** extensie weten we dat het een **afbeelding** is.
2. Klik met de {% include ui.html ui='rc' %} op de afbeelding, kies {% include ui.html ui='naam wijzigen' %} en verander de extensie naar '**.txt**' zodat de computer denkt dat het een **tekstbestand** is.
3. {% include ui.html ui='dc' %} op de afbeelding zodat het opent met een **tekstprogramma**  *(omdat de computer denkt dat het een tekstbestand is)*.  
Wat we nu te zien krijgen is de **computer code** waaruit de afbeelding bestaat.

# Hoe snel kan ik deze website maken?

Ik ga jullie nu laten zien hoe je onderstaande website maakt.  

{% include callout.html type='vraag' content='Hoe lang zal het duren om deze simple Hello world website te maken.' %}

{% include browser.html img='images/hello-world.png' %}

## Zelf proberen

{% include callout.html type='vraag' content='Hoe snel kan je dit zelf?' %}

1. Maak een nieuw **tekstdocument**.
2. Hernoem het document naar {% include filePath.html fileOrPath='index.html' %}, **zorg dat de bestand extensies zichtbaar zijn anders krijg je een dubbele extensie**.
    *Bijvoorbeeld: text.html.txt*  
    Je zal het icoontje zien veranderen van een tekstdocument naar een website icoontje.
3. Op het bestand met **kladblok**.
4. Schrijf **Hello world** en sla het bestand op.
5. Open het bestand met een **webbrowser**.
