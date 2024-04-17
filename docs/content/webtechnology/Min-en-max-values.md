---
title: Min en max values
date: Mon, Mar 25, 2024  4:03:05 PM
---

In CSS stellen min en max values de **minimale en maximale grootte van een element** in. Dit is handig bij het ontwerpen van responsive websites, omdat het elementen kan helpen zich aan te passen aan verschillende schermgroottes en apparaten **zonder media-queries** te moeten gebruiken.

Het werken met min en max values is vaak simpeler *(op een goede manier)* dan werken met media-queries, omdat je per element enkel een minimale of maximale grootte moet instellen, zonder je ontwerp te moeten gaan aanpassen voor meerdere schermformaten.

# Voorbeelden

```css
.alwaysMaxWidth {
    width: 90%;
    max-width: 300px;
}
```

```html
<div class="alwaysMaxWidth">
    Deze elementen zullen een maximale grootte hebben, zolang zullen nooit groter worden dan 300px.<br>
    Dit is zeer handig afbeeldingen die zo groot mogelijk moeten zijn zonder verlies van kwaliteit.
</div>
<img class="alwaysMaxWidth" src="images/big.png">
```

{% include browser.html img='images/min-max-width.gif' %}

# Oefening: Sidebar menu

{% include browser.html img='images/oef-sidebar.gif' %}

Maak een sidebar menu met deze eigenschappen:
- De sidebar neemt **20%** van de **breedte** van de pagina in.
- De sidebar moet **tussen de 130 en 250 pixels breed** blijven.
- De 1e letter van je hoofdtitel heeft een andere kleur, dit doe je met een speciale CSS-selector.
- Voor de ondertitels staat een speciaal ASCII-symbool in een andere kleur. Op [deze website](https://ss64.com/ascii.html) kan je speciale ASCII-symbolen terugvinden.
- De links zijn onderlijnt in een andere kleur.
- Je sidebar staat **verticaal gecentreerd**.