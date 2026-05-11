---
title: De Voeding
created: 2026-05-11 20:56:26 +0200
last_modified: 2026-05-11 22:29:02 +0200
---

> Wordt vaak een **PSU of Power Supply Unit** genoemd.

{% include toggle.html title="Hoe ziet een voeding er uit?" content="
![voeding](images/voeding.jpg){: .frame }

**Waar zit de voeding?**

![voeding](images/voeding-case.jpg){: .frame }
" %}

# Waarom heeft een computer een voeding nodig?

{% include toggle.html title="Waarom kan je een computer niet gewoon rechtstreeks in het stopcontact steken?" content="
Een stopcontact levert **wisselstroom (AC)**.  
Computeronderdelen zijn gemaakt om te werken met lage **gelijkstroom (DC)**.  

Als je een computer rechtstreeks op het stopcontact zou aansluiten:
- Krijgen onderdelen veel te veel spanning
- Zou de stroom voortdurend van richting veranderen
- Zouden componenten beschadigd raken of doorbranden

Daarom gebruikt een computer een voeding (PSU) die:
- De stroom omzet
- De spanning verlaagt
- De stroom veilig verdeelt
" %}

# Spanning

<iframe width="560" height="315" src="https://www.youtube.com/embed/SR3IR8OaNBg?si=sng9loEDrMFpHRuK" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

{% include toggle.html title="Wat zijn spanning en vermogen?" content="
**Spanning (Volt)**  
Spanning geeft aan hoe sterk elektriciteit **duwt**.  
Je kan dit vergelijken met waterdruk in een waterleiding.  
Hoe hoger de spanning hoe krachtiger de elektrische stroom kan bewegen.

**Vermogen (Watt)**  
Vermogen geeft aan hoeveel energie een toestel **gebruikt of levert**.  
Je kan dit vergelijken met hoeveel water per seconde door een waterleiding stroomt.  

**Vergelijking:**
- Spanning (Volt) is de waterdruk.
- Vermogen (Watt) is hoeveel water er effectief beweegt.

**Een hoge spanning betekent niet automatisch hoog vermogen.**  
Vergelijk de spanning en het vermogen van deze vergelijkingen:
- Een dun straaltje water onder hoge druk: *spanning en vermogen?*
- Een grote waterstroom: *spanning en vermogen?*
" %}

{% include toggle.html title="Wat zijn wissel- en gelijkstroom?" content="
**Gelijkstroom (DC)**  
Bij gelijkstroom stroomt elektriciteit altijd in **dezelfde richting**.  
Dat is **stabieler en veiliger** voor elektronische onderdelen.  

**Wisselstroom (AC)**  
Bij wisselstroom **verandert de richting** van de stroom voortdurend.  
Dit is de soort stroom uit het **stopcontact**.  
In Europa verandert die richting 50 keer per seconde.  
Wisselstroom veel praktischer voor:
- Elektriciteit over lange afstanden vervoeren
- Hele steden van stroom voorzien

Wanneer elektriciteit door kabels reist gaat een deel verloren als warmte.  
Bij lange afstanden wil je dus zo weinig mogelijk stroomverlies.
" %}

{% include toggle.html title="Gebruikt een computer AC of DC?" content="
> Gelijkstroom (DC)

De voeding zet daarom **AC uit het stopcontact** om naar **DC voor de computer**.
" %}

## Opdracht: Gelijk- en wisselspanning

Download en maak deze oefening: [Gelijk- en wisselspanning](zelfstandige-opdrachten/gelijkspanning-en-wisselspanning.docx){: .opdracht }

## Opdracht: Spanningen in een computer

1. Hoeveel spanning gebruiken deze componenten?  
  ![Open case](images/spanning-componenten.png)
2. *Onderzoeksvraag:* Waarom zou een videokaart meer stroom nodig hebben dan een USB-stick?
3. Wat is het vermogen van deze toestellen?
  3.1 LED-lamp
  3.2 Laptop 
  3.3 Gaming PC

# Efficiëntie

{% include toggle.html title="Een voeding haalt 500W uit het stopcontact, maar levert maar 425W aan de computer. Wat gebeurt er met de rest?" content="
De overige energie gaat vooral verloren als **warmte**.  

Geen enkele voeding werkt perfect efficiënt.  
Daarom hebben voedingen **ventilatoren, koeling, heatsinks**.
" %}

{% include toggle.html title="Waarom hechten datacenters veel belang aa efficiente voedingen?" content="
Datacenters bevatten **duizenden** computers en servers.  
Zelfs kleine energieverliezen worden daardoor enorm groot.

Efficiënte voedingen zijn belangrijk omdat ze:
- Minder elektriciteit verspillen
- Minder warmte produceren
- Lagere elektriciteitskosten geven
- Minder zware koeling nodig hebben
- Beter zijn voor het milieu

Minder warmte betekent ook:
- Minder airconditioning
- Minder risico op oververhitting
- Betrouwbaardere servers
" %}

## Certificaten


# Soorten voedingen 


