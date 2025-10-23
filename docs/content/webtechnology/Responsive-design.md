---
title: Responsive Design
last_modified: 2025-05-09 15:40:02 +0200
created: 2025-04-04 10:48:04 +0200
---

# Wat is responsive design?

<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vSnFaYYHLrTxCS8w7qM_RWBAPidlXrqNC8wq69L0Y17hAPQc3yUAL5dvAj7R1BKdA/embed?start=false&loop=false&delayms=3000" frameborder="0" width="1280" height="515" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>

# Hoe maak je een website responsive?

### Min- en max-values

```css
img {
  width: 90%;
  max-width: 300px;
}

img {
  width: 50%;
  mix-width: 50px;
}
```

### Media queries: Oriëntatie (Liggend/Portret)

```css
/* Portretmodus */
@media only screen and (orientation: portrait) {
  body {
    background-color: black;
  }
}

/* Liggende */
@media only screen and (orientation: landscape) {
  body {
    background-color: white;
  }
}
```

### Media queries: Scherm breedte

```css
/* Schermen breder van 700px */
@media screen and (min-width: 700px) {
  body {
    background-color: black;
  }
}

/* Schermen tussen 530px en 700px breed */
@media screen and (max-width: 700px) and (min-width: 530px) {
  body {
    background-color: grey;
  }
}

/* Schermen kleiner dan 530px breed */
@media (max-width: 530px) {
  body {
    background-color: white;
  }
}
```

# Praktische tips

## Elementen tonen en verbeteren

Je kan elementen **verbergen** met `display:none`, bijvoorbeeld bij een dropdown of mobiele navigatie.

```css
.hidden {
  display: none;
}
```

Je kan elementen terug zichtbaar maken met:

- `display: block`: Toont het element als een blok. Het neemt de hele breedte in van zijn container.  
   **Zoals `<div>`-elementen.**
- `display: inline`: Toont het element naast andere elementen zonder een nieuwe regel te starten.  
   **Zoals `<span>`-elementen.**

## Fullscreen overlay

Fullscreen overlays worden in webdesign vaak gebruikt om **fullscreen menu's of pop-ups** te maken.

```css
.fixed-button {
  position: fixed;
  top: 0px;
  right: 0px;
  z-index: 1;
  background: black;
  opacity: 0.9;
}
```

- `position: fixed` zet een element vast op het scherm, los van andere elementen. Het blijft altijd op dezelfde plek, ook als je scrolt. Het wordt gepositioneerd ten opzichte van het browservenster, niet van een ander element.
- Met `top`, `bottom`, `left` en `right` kan je de plaats bepalen.
- De `z-index` bepaalt welk element bovenop komt te liggen als meerdere elementen elkaar overlappen. Een element met een hogere z-index ligt bovenop een element met een lagere z-index. De standaard z-index is 0.

# Opdracht: Responsive design

Maak een nieuwe website via de regels van responsive design.  
Je website heeft deze zaken:

- Maak 2 tekstblokken en daarin tekst van 12 pixels groot.
  - De eerste neemt 10% van de breedte van de pagina in, de tweede 30%.
  - Als het scherm **horizontaal** staat _(het is breder dan het hoog is, zoals desktops en laptops)_, staan de tekstblokken naast elkaar.
  - Als het scherm **verticaal** staan _(het is hoger dan het breed is, zoals bij smartphones)_, staan de tekstblokken onder elkaar.
- Laat de tekstgrootte aanpassen aan de hand van de breedte van het scherm:
  - Schermen **kleiner dan 300 pixels** -> tekstgrootte van **30 pixels**.
  - Schermen **tussen 300 en 600 pixels** -> tekstgrootte van **20 pixels**.
- **Navigatie balk** die overgaat in een **hamburger menu** wanneer de pagina kleiner is dan 500 pixels.
  - De **navigatie balk** bevat **links een titel** en **rechts links**.
  - Het **hamburger menu** opent een **fullscreen overlay menu** waarin de titel bovenaan staat, en de links onder elkaar. Het fullscreen overlay menu openen doe je best via **JavaScript**.
