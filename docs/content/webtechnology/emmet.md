---
title: Emmet
created: 2026-02-12 10:53:01 +0100
last_modified: 2026-02-12 10:53:01 +0100
---

# Wat is Emmet?

HTML schrijven is vaak repetitief: veel tags, veel geneste structuren, 
veel typwerk. Emmet is een hulpmiddel dat dit werk drastisch versnelt.

Emmet is een plugin (ingebouwd in o.a. VS Code) waarmee je **via afkortingen automatisch HTML- en CSS-code genereert**.

## Voordelen

- Sneller werken
- Minder typfouten
- Focus op structuur en inhoud, niet op syntax

Emmet is standaard ingebouwd in de meeste code editors, zo niet in er waarschijnlijk een Emmet plugin die je kan gebruiken.

# Hoe gebruik je Emmet?

1. Typ een Emmet-afkorting
2. Druk op Tab of Enter
3. De code wordt gegenereerd

Emmet is **contextgevoelig**.  
Wat je typt is belangrijk, maar **waar je het typt** is minstens even belangrijk.

**Dezelfde afkorting** kan dus iets totaal **anders opleveren** afhankelijk van:
- Of je in een HTML-bestand zit
- Of je in een CSS-bestand zit
- Of je binnen een bepaald HTML-element werkt
- Of je in een attribuut zit

## De Bouwstenen

Belangrijkste bouwstenen:  
{% raw %}
| Shortcut | Functie |
| ---- | --- |
| `>`  | child *(geneste elementen)* |
| `+`  | sibling *(naast elkaar)* |
| `*`  | vermenigvuldiging |
| `.`  | class |
| `#`  | id |
| `{}` | tekstinhoud |
| `[]` | attributen |
| `$`  | nummering |
{% endraw %}

Iedereen krijgt een bouwsteen toegewegen:  
1. Surf naar [https://www.emmet.io/](https://www.emmet.io/) *(de officiele website)*.
2. Zoek uit wat de functie van je bouwsteen is.
3. Geef een kleine demo aan de klas.

## Groepen `()`

Groepen zorgen ervoor dat je structuur niet uit elkaar valt als een kaartenhuis zodra je begint te vermenigvuldigen of siblings toe te voegen. Denk eraan als **wiskunde voor HTML: eerst wat tussen de haakjes staat, daarna de rest**.

Zonder groepering werkt Emmet strikt van **links naar rechts**. **Met groepering zeg jij: deze blokken horen samen**.

**Simpel voorbeeld:**
Emmet zonder groepering:
```html
div>h1+p*2
```
Geeft:
```html
<div>
  <h1></h1>
  <p></p>
  <p></p>
</div>
```

Emmet met groepering:
```html
div>(h1+p)*2
```
Geeft:
```html
<div>
  <h1></h1>
  <p></p>
  <h1></h1>
  <p></p>
</div>
```

**Praktisch voorbeeld**
Stel je wil dit:
```html
<section>
  <div>
    <h3></h3>
    <p></p>
  </div>
  <div>
    <h3></h3>
    <p></p>
  </div>
</section>
```

Dit kan enkel via groeperingen:
```html
section>div*2>(h3+p)
```
Emmet begrijpt nu:
1. Maak een section
2. Maak daarin 2 divs
3. In elke div komt het blok (h3+p)
Haakjes zorgen ervoor dat h3+p binnen elke div terechtkomt.

Wanneer **moet** je groeperen?
- Wanneer je meerdere siblings samen wil vermenigvuldigen
- Wanneer je een complexe structuur als één geheel wil behandelen
- Wanneer je vermenigvuldiging niet alleen op het laatste element mag slaan

**Wat is het verschil tussen deze 2 Emmet regels?**
```html
div>(h1+p)*2
```
```html
div>h1+p*2
```

# Oefeningen

Probeer de gegeven HTML-code zo efficiënt mogelijk te schrijven.

## Niveau 1: Opwarming

### Oef 1.1: Element

```html
<p></p>
```

### Oef 1.2: Element met class

```html
<div class="container"></div>
```

### Oef 1.3: Element met id

```html
<section id="about"></section>
```

### Oef 1.4: Element met tekst

```html
<h1>Welkom</h1>
```

## Niveau 2: Meerdere elementen

### Oef 2.1: Siblings

```html
<h1></h1>
<p></p>
```

### Oef 2.2: Genest

```html
<ul>
  <li></li>
</ul>
```

### Oef 2.3: Meerdere kinderen

```html
<ul>
  <li></li>
  <li></li>
  <li></li>
</ul>
```

## Niveau 3: Combinaties

### Oef 3.1: Structuur met siblings én nesting

```html
<div class="card">
  <h2></h2>
  <p></p>
</div>
```

### Oef 3.2: Navigatie

```html
<nav>
  <ul>
    <li></li>
    <li></li>
    <li></li>
  </ul>
</nav>
```

### Oef 3.3: Links

```html
<ul>
  <li><a href="#"></a></li>
  <li><a href="#"></a></li>
  <li><a href="#"></a></li>
</ul>
```

## Niveau 4: Attributen en tekst

### Oef 4.1: Link met tekst

```html
<a href="contact.html">Contacteer ons</a>
```

### Oef 4.2: Afbeelding

```html
<img src="image.jpg" alt="Beschrijving">
```

### Oef 4.3: Genummerde classes

```html
<ul>
  <li class="item-1"></li>
  <li class="item-2"></li>
  <li class="item-3"></li>
  <li class="item-4"></li>
</ul>
```

## Niveau 5: Groepering

### Oef 5.1: Header + nav

```html
<header>
  <h1></h1>
  <nav>
    <ul>
      <li></li>
      <li></li>
    </ul>
  </nav>
</header>
```

### Oef 5.2: Artikelstructuur

```html
<article>
  <h2></h2>
  <p></p>
  <p></p>
  <a href="#"></a>
</article>
```

## Niveau 6: Uitdagingen

### Oef 6.1: Drie kaarten

```html
<section class="cards">
  <div class="card">
    <h3></h3>
    <p></p>
    <a href="#"></a>
  </div>
  <div class="card">
    <h3></h3>
    <p></p>
    <a href="#"></a>
  </div>
  <div class="card">
    <h3></h3>
    <p></p>
    <a href="#"></a>
  </div>
</section>
```

### Oef 6.2: Complexe layout

```html
<div class="container">
  <header>
    <h1></h1>
  </header>
  <main>
    <section>
      <h2></h2>
      <p></p>
      <p></p>
    </section>
  </main>
  <footer>
    <p></p>
  </footer>
</div>
```

# Wedstrijd: Wie wordt de Emmet KONING?

Je zal HTML-code te zien krijgen en moet deze zo efficiënt weten te schrijven via Emmet.

## Puntensysteem

| --- | --- |
| Je kan de gegeven code schrijven via Emmet | `+1 punt` |
| Je kan de gegeven code schrijven in de **kortste expressie** | `+1 punt` |
| Je kan **als snelste** de gegeven code typen via Emmet in **1 regel** | `+ 1 punt` |
