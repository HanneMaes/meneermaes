---
title: Het If-statement
last_modified_at: 2025-09-03 14:40:54 +0200
date: 2024-06-05 10:59:12 +0200
---

Maak een webapp met een **textfield** en een **knop**.

{% include browser.html img='images/if-1.png' width='200px' %}

```html
<form id="formulier">
	<label class="formTitle">Geef een getal:</label><br>
	<input type="text" id="tekstveldGetal" placeholder="0">
</form>

<a id="knopGetal" href="#">Knop</a>

<div id="paginaText"></div>
```

# If-statement

Voeg deze JavaScript code toe om een bericht te tonen als het getal 0 is.
	
{% include browser.html img='images/if-2.png' width='200px' %}

```javascript
document.getElementById("knopGetal").addEventListener("click", function () {

	// haal de waarde uit het tekstveld
	let getal = document.getElementById("tekstveldGetal").value;
	console.log(getal);

	// als het getal 0 is, tonen we een bericht op de pagina
	if (getal == 0) {
		document.getElementById("paginaText").innerHTML += "Het getal is 0!";
	}
});
```

# If-else-statement

Als het getal 0 is, tonen we een bericht op de pagina, zo niet tonen we een ander bericht.

{% include browser.html img='images/if-2.png' width='200px' %}
{% include browser.html img='images/if-3.png' width='200px' %}

```javascript
document.getElementById("knopGetal").addEventListener("click", function () {

	// haal de waarde uit het tekstveld
	let getal = document.getElementById("tekstveldGetal").value;
	console.log(getal);

	// als het getal 0 is, tonen we een bericht op de pagina
	// zo niet tonen we een ander bericht
	if (getal == 0) {
		document.getElementById("paginaText").innerHTML += "Het getal is 0!";
	} else {
		document.getElementById("paginaText").innerHTML += "Het getal is niet 0! <br>";
	}
});
```

# If-else-if-statement

Als het getal 0 is, tonen we "Het getal is 0!".  
Als het getal groter dan 0 is, tonen we "Het getal is POSITIEF!".  
Zo niet tonen we "Het getal is NEGATIEF!""

{% include browser.html img='images/if-2.png' width='200px' %}
{% include browser.html img='images/if-4.png' width='200px' %}
{% include browser.html img='images/if-5.png' width='200px' %}

```javascript
document.getElementById("knopGetal").addEventListener("click", function () {

	// haal de waarde uit het tekstveld
	let getal = document.getElementById("tekstveldGetal").value;
	console.log(getal);

	// als het getal 0 is, tonen we "Het getal is 0!"
	// als het getal groter dan 0 is, tonen we "Het getal is POSITIEF!"
	// zo niet tonen we "Het getal is NEGATIEF!""
	if (getal == 0) {
		document.getElementById("paginaText").innerHTML = "Het getal is 0!";
	} else if (getal > 0) {
		document.getElementById("paginaText").innerHTML = "Het getal is POSITIEF";
	} else {
		document.getElementById("paginaText").innerHTML = "Het getal is NEGATIEF";
	}
});
```

# Code optimaliseren

Momenteel doen we 3 keer `document.getElementById("paginaText").innerHTML`, elke keer dat we deze code uitvoeren kost dit een beetje **tijd en computer resources**.

We kunnen onze code optimaliseren, en onze webapp sneller maker door dit maar 1 keer uit te voeren en **op te slaan in een variable**:  
`let tekst = document.getElementById("paginaText")`

Onze code ziet er dan als volgt uit:
```javascript
document.getElementById("knopGetal").addEventListener("click", function () {

	// haal de waarde uit het tekstveld
	let getal = document.getElementById("tekstveldGetal").value;
	console.log(getal);

	// de <div> opslaan in een variabele
	let tekst = document.getElementById("paginaText");

	// if-statement
	if (getal == 0) {
		tekst.innerHTML = "Het getal is 0!";
	} else if (getal > 0) {
		tekst.innerHTML = "Het getal is POSITIEF";
	} else {
		tekst.innerHTML = "Het getal is NEGATIEF";
	}
});
```

# InnerHTML met HTML-tags

We kunnen via de `.innerHTML` methode ook **HTML-code toevoegen** aan de pagina.

{% include browser.html img='images/if-6.png' width='200px' %}

```javascript
document.getElementById("knopGetal").addEventListener("click", function () {

	let getal = document.getElementById("tekstveldGetal").value;
	console.log(getal);

	let tekst = document.getElementById("paginaText");

	if (getal == 0) {
		tekst.innerHTML += "Het getal is 0! <br>";
	} else if (getal > 0) {
		tekst.innerHTML += "Het getal is <strong>POSITIEF</strong> <br>";
	} else {
		tekst.innerHTML += "Het getal is <strong>NEGATIEF</strong> <br>";
	}

});
```
