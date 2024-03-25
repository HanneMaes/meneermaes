---
title: 'Responsive design: CSS'
layout: default
date: Wed, Mar 20, 2024  3:36:23 PM
---

# Media queries

Media queries stellen ons in staat om **specifieke CSS-regels** toe te passen op basis van de **eigenschappen van het apparaat**.

![](images/media-query.gif)

```html
<body>
	Dit is mijn <span class="text"></span> website.
</body>
```

```css
body {
    font-size: 30px;
}

.text::before {
    content: 'desktop';
    color: goldenrod;
    margin-left:  10px;
    margin-right: 10px;
}

/* gebruik deze styling als het scherm 500px of minder breed is */
@media screen and (max-width: 500px) {
    body {
        background-color: black;
        color: white;
    }
    
    .text::before {
        content: 'mobile';
    }
}
```

## Soorten media quaries

### Scherm breedte

```css
/* Schermen kleiner dan of gelijk aan 768px breed */
@media only screen and (max-width: 768px) {
  /* CSS-regels */
}

/* Schermen groter dan 768px breed */
@media only screen and (min-width: 1000px) {
  /* CSS-regels */
}
```

### Oriëntatie (Liggend/Portret)

```css
/* Portretmodus */
@media only screen and (orientation: portrait) {
  /* CSS-regels */
}

/* Liggende */
@media only screen and (orientation: landscape) {
  /* CSS-regels */
}

```

## Media queries combineren

Het is mogelijk meerdere **media queries** met elkaar te **combineren**.

![alt text](images/media-query-combine.gif)

```html
<body>
    <p class="orientatie">Oriëntatie</p>
    <p class="text">Font-size</p>
</body>
```

```css
body {
    font-size: 30px;
    color: grey;
}

/**************/
/* orientatie */
/**************/

/* Portretmodus */
@media only screen and (orientation: portrait) {
    body {
        background-color: black;
        color: white;
    }
    .orientatie::after {
        content: ': portrait';
    }
}
  
/* Liggende */
@media only screen and (orientation: landscape) {
    body {
        background-color: white;
        color: black;
    }
    .orientatie::after {
        content: ': landscape';
    }
}

/**************/
/* screensize */
/**************/

@media screen and (min-width: 700px) {
    .text {
        font-size: 100px;
    }
    .text::after {
        content: ': 100px';
    }
}

@media screen and (max-width: 700px) and (min-width: 530px) {
    .text {
        font-size: 80px;
    }
    .text::after {
        content: ': 80px';
    }
}

@media (max-width: 530px) {
    .text {
        font-size: 30px;
    }
    .text::after {
        content: ': 30px';
    }
}
```

# Developer tools

# Oefening 01: Row vs column

# Oefening 02: Navbar vs hamburger menu