---
title: Geavanceerde CSS-Selectors
last_modified: 2024-10-18 16:19:48 +0200
created: 2024-10-18 14:01:36 +0200
---

> Test onderstaande code uit, en probeer te achterhalen wat ze doen

# Links: hover & visited

```html
<a href="https://www.meneermaes.be/">Link 1</a>
<a href="https://www.meneermaes.be/">Link 2</a>
<a href="https://www.meneermaes.be/">Link 3</a>
<a href="https://www.meneermaes.be/">Link 4</a>
```

```css
a:hover {
    color: red;

}
a:visited {
    color: green;
}
```

# First-letter & first-line

```html
<p class="eersteletter">Eerste letter</p>
<p class="eerstelijn">Eerste lijn.<br>Tweede lijn.</p>
```

```css
.eersteletter::first-letter {
    color: red;

}
.eerstelijn::first-line {
    color: green;
}
```

# Before & after


```html
Aankoop prijs: <span class="euro">100</span>
```

```css
.euro::before {
    content: '€';
    color: orange;
}

.euro::after {
    content: '!';
    color: red;
}
```
