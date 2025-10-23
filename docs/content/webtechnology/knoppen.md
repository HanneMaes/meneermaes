---
title: Knoppen
last_modified: 2024-10-18 12:48:19 +0200
created: 2024-10-18 12:28:08 +0200
---

#  \<button \> vs  \<a\>

```html
<button>Button</button>
<a href="#">Link</a>
```
{% include browser.html img='images/knop-vs-link.png' %}

In HTML zijn zowel de `<button>`- als `<a>`-elementen bedoeld om interactieve elementen op een webpagina te creëren, maar ze hebben verschillende doeleinden en gedragingen.

- `<a>`-elementen worden gebruikt om **hyperlinks** te maken, wat betekent dat het wordt gebruikt om van de ene webpagina naar de andere te linken.
- `<button>`-elementen worden meestal gebruikt in **formulieren in combinatie met PHP** om interactieve functionaliteit aan webpagina's toe te voegen.

{% include callout.html type='tip' content='
Aangezien de meeste knoppen op webpagina’s dienen om naar andere pagina’s te gaan we meestal `<a>`-elementen gebruiken.
' %}

Een ander voordeel is dat `<a>`-elementen minder opmaak hebben en dus **makkelijker zelf te stylen** zijn.  
Een link is enkel blauw met een underscore, terwijl een button heeft meer opmaak, en is dus moeilijker zelf te stylen.

{% include browser.html img='images/knop-vs-link.png' %}

# Hover & visited

```css
a:hover {
    color: red;
}

a:visited {
    color: orange;
}
```

# Hover animaties

```css
a {
    transition: 0.5s;
}

a:hover {
    color: red;
}
```

# Opdracht: Knoppen ontwerpen

1. Maak een website met 3 `<a>`-elementen en 3 `<button>`-elementen.
2. Geef elke knop een **uniek design**.  
    Op deze pagina kan je informatie vinden over hoe je knoppen kan stylen: [https://www.w3schools.com/css/css3_buttons.asp](https://www.w3schools.com/css/css3_buttons.asp)
3. Gebruik **minstens 3 verschillende webfonts**.
4. Geef elke knop een **uniek hover effect**.

{% include punten-csv.html data='knoppen' %}

# Uitdaging: Knop namaken

1. Surf naar [https://dribbble.com/](https://dribbble.com/) en zoek naar het woord **button**.
2. Kies een mooie knop.
3. Download de afbeelding of video van de knop en voeg hem toe aan je website.
4. Voeg een **nieuwe knop** toe aan je website, en probeer de knop die je gevonden hebt zo goed mogelijk na te maken.
