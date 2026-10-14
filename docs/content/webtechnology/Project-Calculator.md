---
title: Project Calculator
last_modified: 2026-10-14 15:19:07 +0200
created: 2025-04-24 16:37:03 +0200
---

Maak een webapp waarbij je zaken kan invullen, er dan berekeningen gemaakt worden en deze getoond worden.

Maak je project zo **mooi en overzichtelijk** mogelijk.

{% include browser.html img='images/calculator-project-2.gif' %}

{% include browser.html img='images/calculator-project-1.png' %}

# Stap 1: Winst berekenen

Je start een kledingmerk en je schrijft een webapp om te bereken hoeveel je moet vragen voor je producten.  
Start met een formulier dat je in kan vullen, wanneer je op de knop **Calculate profits** klikt, verschijnen de winsten.

{% include browser.html img='images/price-calculator.png' width='400px' %}
{% include browser.html img='images/price-calculator-2.png' width='400px' %}

Zo bereken je de winst:
```
Profit = Manufacturing costs - Selling price
```

# Stap 2: Shipping

Je wil ook online beginnen verschepen, maar het shippen van je kleding kost je extra geld, voeg deze berekening toe aan je webapp.  

{% include browser.html img='images/price-calculator-3.png' width='400px' %}
{% include browser.html img='images/price-calculator-4.png' width='400px' %}

Zo bereken je de winst rekening houdend met de shipping costs:
```
Profit = Manufacturing costs - Selling price - Shipping costs
```

# Stap 3: Target profit

Voeg de mogelijkheid toe om in te vullen hoeveel winst je wil maken, die heet de **target profit**.  
Pas de kleur van de tekst aan:
- <span class="goodText">Groen</span> bij een winst <span class="goodText">hoger</span> van de target profit.
- <span class='badText'>Rood</span> bij een winst <span class='badText'>lager</span> van de target profit.
- <span class='blueText'>Blauw</span> als de winst <span class='blueText'>exact</span> de target profit is.

{% include browser.html img='images/price-calculator-5.png' width='400px' %}

{% include callout.html type='tip' content='Om exact 15 euro winst te maken op mijn shirt heb ik de prijs van de shirt verhoogd naar 10 euro.' %}
