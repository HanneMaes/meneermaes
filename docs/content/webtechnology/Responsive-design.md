---
title: Responsive Design
last_modified_at: 2025-05-09 09:48:49 +0200
date: 2025-04-04 10:48:04 +0200
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

# Opdracht: Responsive design

Maak een nieuwe website via de regels van responsive design.  
Je website heeft deze zaken:

- **Navigatie balk** die overgaat in een **hamburger menu of bottom navigation**.
- Landing page met duidelijke **call to action**.
