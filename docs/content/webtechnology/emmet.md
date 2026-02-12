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

# De Bouwstenen

Belangrijkste bouwstenen:
| Shortcut | Functie |
| --- | --- |
| `>` | child *(geneste elementen)* |
| `+` | sibling *(naast elkaar)* |
| `*` | vermenigvuldiging |
| `.` | class |
| `#` | id |
| `{}` | tekstinhoud |
| `[]` | attributen |

Iedereen krijgt een bouwsteen toegewegen:  
1. Surf naar [https://www.emmet.io/](https://www.emmet.io/) *(de officiele website)*.
2. Zoek uit wat de functie van je bouwsteen is.
3. Geef een kleine demo aan de klas.

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
