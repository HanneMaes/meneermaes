---
title: Responsive design met JavaScript
date: 2024-04-16 21:02:37 +0200
---

Het gebruik van **CSS** voor het maken van een responsieve website is over het algemeen de **beste aanpak** omdat CSS specifiek is ontworpen voor het stylen van webpagina's, inclusief het aanpassen van lay-outs op verschillende schermgroottes. **Het laden van CSS-bestanden is sneller en efficiënter dan het uitvoeren van JavaScript-code.**

Maar, in bepaalde situaties kan het nuttig zijn om JavaScript te gebruiken voor **aanvullende responsieve functionaliteit**.

Maak onderstaand voorbeeld na:

{% include browser.html img='images/responsive-js.png' %}

```javascript
// wacht tot de DOM volledig geladen is
document.addEventListener("DOMContentLoaded", function() {

    let siteWidth = window.innerWidth;
    let siteHeight = window.innerHeight;
    
    // width & height laten zien op de pagina
    document.getElementById("width").innerHTML = siteWidth;
    document.getElementById("height").innerHTML = siteHeight;
    
    // portrait or landscape
    if (siteHeight > siteWidth) {
        document.getElementById("landscapeOrPortrait").innerHTML = "Portrait";
    } else {
        document.getElementById("landscapeOrPortrait").innerHTML = "Desktop";
    }

});
```

```html
<span id="width"></span> X <span id="height"></span>
<br>
<span id="landscapeOrPortrait"></span>
```

{% include callout.html type='question' content='Als je deze code uittest zal je merken dat deze niet optimaal is. Onderstaande code zal dit probleem oplossen.' %}

```javascript
// wacht tot de DOM volledig geladen is
document.addEventListener("DOMContentLoaded", function() {

    function screenChange() {
        // width & height opvragen
        let siteWidth = window.innerWidth;
        let siteHeight = window.innerHeight;
        
        // width & height laten zien op de pagina
        document.getElementById("width").innerHTML = siteWidth;
        document.getElementById("height").innerHTML = siteHeight;
        
        // portrait or landscape
        if (siteHeight > siteWidth) {
            document.getElementById("landscapeOrPortrait").innerHTML = "Portrait";
        } else {
            document.getElementById("landscapeOrPortrait").innerHTML = "Desktop";
        }
    }
    window.addEventListener('resize', screenChange); // Voer de functie uit wanneer het scherm veranderd
    screenChange(); // Voer de functie uit om de eerste keer de waarden te laten zien

});
```

{% include browser.html img='images/responsive-js-update.gif' %}

Deze code zorgt ervoor dat wanneer we de grootte van het scherm aanpassen onze pagina geüpdatet zal worden.
1. Zet de code om de grootte van het scherm te vinden in een functie.  
    `function screenChange()`
2. Voer de functie uit elke keer als de grootte van de pagina veranderd.  
    `window.addEventListener('resize', screenChange);`
3. Nu zal de code enkel uitgevoerd worden wanneer we de pagina van grootte veranderen, en dus niet wanneer we de pagina openen. Daar om moeten we de functie ook nog eens uitvoeren.  
    `screenChange();`

# Oefening: Navbar & hamburger menu

{% include callout.html type='oef' content='Werk verder van "oefening: Responsive CSS".' %}

{% include browser.html img='images/oef-gellery-nav.png' %}
{% include phone.html img='images/oef-gallery-hamburger.png' %}

Geef je gallery een **responsive menu**:
- Desktop: 
    - Een **horizontale** navbar.
- Mobile: 
    - Een **hamburger menu** dat een **full-screen menu** opent.

{% include callout.html type='info' content='Maak je website resonsive met CSS, niet met JavaScript. JavaScript gebruik je alleen wanneer je zaken niet kan doen met CSS!' %}

{% include callout.html type='tip' content='Met onderstaande CSS-regel kan je een HTML-element verwijderen.' %}

```css
.hide {
    display: none;
}
```