---
title: "Neutral Html Tags:<br> div & span"
last_modified_at: 2024-10-18 09:41:33 +0200
date: 2024-10-18 09:10:08 +0200
---

Zowel `<div>` als `<span>` zijn veelgebruikte HTML-elementen die dienen als "containers" om inhoud te structureren.

Ze zijn **neutraal** en hebben **geen standaard visuele opmaak** *(zoals kleur, grootte, of marges)*. Hierdoor functioneren ze als een leeg canvas, waarop je met CSS **volledige controle** hebt om stijlen toe te passen.

# Belangrijkste verschillen

Hoewel beide elementen gebruikt worden om inhoud te groeperen, zijn er belangrjke verschillen:
- `<span>` is een **inline-element**:
    Dat nbetekent dat het wordt weergegeven binnen de normale stroom van een tekstregel. 
    Het is geschikt voor het toepassen van stijlen op **woorden, zinnen, of delen van een tekst**.
- `<div>` is een **blok-element**
    Dat betekent dat het **altijd een nieuwe regel begint en de volledige breedte van zijn oudercontainer inneemt**.
    Het wordt vaak gebruikt om secties van een webpagina te definiëren of om groepen van elementen samen te voegen.

## Test zelf het verschil

Start met het maken van deze HTML-pagina.  
Je zal niets zien van de `<span>` en `<div>` elementen, dit komt omdat het **blanco** elementen zijn, die **geen standaard visuele opmaak** hebben. Dit zorgt ervoor dat je vanaf nul kunt beginnen met het ontwerpen.

```html
<p>
    Dit is <span class="styling">span element.</span>
</p>
<p>
    Dit is <div class="styling">div element.</div>
</p>
```

Je zult ze pas zien of opmerken op je webpagina als je ze zelf stijlen met CSS: 

```css
p {
    background-color: yellow;
}

.styling {
    background-color: red;
}
```

# Combineren met andere elementen

## `<span>` combineren

```html
<h1>SPAN combineren met <span class="spanNaam">andere</span> elementen</h1>

<div class="divNaam">
    Dit is een DIV.<br>
    Dit is een <span class="spanNaam">SPAN</span>.
</div>
```

```css
.divNaam {
    background-color: cyan;
}

.spanNaam {
    background-color: pink;
}

.divTwee {
    background-color: black;
    color: white;
}
```

## `<div>` combineren

```html
<h1>SPAN combineren met <span class="spanNaam">andere</span> elementen</h1>

<div class="divNaam">
    Dit is een DIV.<br>
    Dit is een <span class="spanNaam">SPAN</span>.

    <div class="divTwee">Dit is een 2e div</div>

</div>
```

```css
.divNaam {
    background-color: cyan;
}

.spanNaam {
    background-color: pink;
}

.divTwee {
    background-color: black;
    color: white;
}
```

## Blijven gaan!

```html
<h1>SPAN combineren met <span class="spanNaam">andere</span> elementen</h1>

<div class="divNaam">
    Dit is een DIV.<br>
    Dit is een <span class="spanNaam">SPAN</span>.

    <div class="divTwee">Dit is een 2e div, met <span class="spanNaam">terug</span> een span</div>

</div>
```

```css
.divNaam {
    background-color: cyan;
}

.spanNaam {
    background-color: pink;
}

.divTwee {
    background-color: black;
    color: white;
}
```
