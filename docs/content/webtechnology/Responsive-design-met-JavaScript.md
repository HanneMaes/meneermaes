---
title: Responsive design met JavaScript
last_modified: 2024-05-03T07:12:37
created: 2024-04-16 21:02:37 +0200
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

## Tips

{% include callout.html type='tip' content='Maak je website resonsive met CSS, niet met JavaScript. JavaScript gebruik je alleen wanneer je zaken niet kan doen met CSS!' %}

### Display

{% include callout.html type='tip' content='Met "display: none;" kan je een HTML-element verwijderen.' %}

```css
.hide {
    display: none;
}
```

De display-eigenschap in CSS bepaalt hoe een element wordt weergegeven.
- 'none': Het element wordt **niet weergegeven** op de pagina, alsof het niet bestaat.
- 'block': Het element wordt weergegeven als een block en neemt standaard de volledige breedte van zijn container in, waardoor het dit element niet op dezelfde regels zal weergegeven worden.  
Een `<div>` heeft `display: block;`.
- 'inline': Het element staat op dezelfde regel en neemt alleen zoveel breedte in als nodig is.  
Een `<span>` heeft `display: inline;`.
- 'inline-block': Combineert de eigenschappen van inline en block. Het element wordt weergegeven in dezelfde regel als omliggende inhoud, maar kan ook breedte en hoogte hebben zoals een block.

### Z-index

{% include callout.html type='tip' content='Met z-index kan je elementen over of onder elkaar laten komen.' %}

```css
z-index: 2;
```

Elementen zonder z-index hebben automatisch een standaard z-index van 0. Hoe hoger de waarde van de z-index, hoe meer naar voren het element wordt geplaatst. Dit betekent dat **een element met een z-index van 2 boven een element met een z-index van 1 wordt geplaatst**.

Belangrijk om te weten is dat z-index niet werkt op elementen die position static hebben.