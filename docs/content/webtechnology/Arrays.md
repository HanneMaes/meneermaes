---
title: Arrays
last_modified_at: 2025-05-23 13:15:25 +0200
date: 2025-05-23 11:58:10 +0200
---

> Een array is een lijst van waarden 

# Arrays gebruiken

## Declaratie
```javascript
let list = ["Brendan Eich", "ECMAScript", "Node.js"];
```

In JavaScript kunnen types zelfs gemengd voorkomen in een array:
```javascript
let list = [1995, true, "Brendan Eich", 10, "ECMAScript", "Node.js"];
```

Een lege array kun je als volgt **aanmaken**:
```javascript
let list = []
```

## Een element uit een array opvragen

```javascript
let list = [1995, true, "Brendan Eich", 10, "ECMAScript", "Node.js"];
console.log(list[0]); // Geeft als uitvoer: 1995
```

Gaan we met onze index voorbij het laatste element van de array, dan krijgen we in JavaScript geen foutmelding, maar bekomen we als waarde `undefined`:
```javascript
let list = [1995, true, "Brendan Eich", 10, "ECMAScript", "Node.js"];
console.log(list[99]); // Geeft als uitvoer: undefined
```

Willen we een element terugvinden in een array, dan kunnen we daarvoor de methode indexOf gebruiken. IndexOf Geeft de index van de gezochte waarde. Komt het gezochte element niet voor in de array, dan retourneert indexOf de waarde -1:

```javascript
let list = [1995, true, "Brendan Eich", 10, "ECMAScript", "Node.js"];
console.log(list.indexOf(1995)); // Geeft als uitvoer: 0
console.log(list.indexOf("Brendan Eich")); // Geeft als uitvoer: 1
console.log(list.indexOf("Brave Browser")); // Geeft als uitvoer: -1
```

## Een element in een array wijzigen

```javascript
let list = [1995, true, "Brendan Eich", 10, "ECMAScript", "Node.js"];
list[0] = "Netscape";
console.log(list); // Geeft als uitvoer: [1995, true, "Brendan Eich", 10, "ECMAScript", "Node.js"]
```

## De lengte van een array opvragen

```javascript
let list = [1995, true, "Brendan Eich", 10, "ECMAScript", "Node.js"];
console.log(list.length); // Geeft als uitvoer: 6
```

## Elementen toevoegen en verwijderen

Een element **toevoegen** aan het **einde** van een array:
```javascript
let list = [1995];
list.push("Electron");
console.log(list); // Geeft als uitvoer: [1995, "Electron"]
```

Een element **verwijderen** aan het **einde** van een array:
```javascript
let list = [1995, "Electron"];
list.pop();
console.log(list); // Geeft als uitvoer: [1995]
```

Een element **verwijderen** aan het **begin** van een array:
```javascript
let list = [1995, "Electron"];
list.shift();
console.log(list); // Geeft als uitvoer: ["Electron"]
```

Een element **toevoegen** aan het **begin** van een array:
```javascript
let list = [1995, "Electron"];
list.unshift("JavaScript is not Java");
console.log(list); // Geeft als uitvoer: ["JavaScript is not Java", 1995, "Electron"]
```

## Over alle elementen van een array loopen

```javascript
let list = [1995, "Electron"];
let text;
for (var i in list) {
  text += list[i]
}
console.log(text); // Geeft als uitvoer: 1995Electron
```


# Oefening op het gebruik van arrays

Tijdens deze oefening gaan we een lijst laten groeien en krimpen vanuit JavaScript

{% include browser.html img='images/arraysoef.gif' %} 

Start met deze code:
```html
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Document</title>
</head>
<body>

   <!-- formulier -->
   <form>
      <label>Toe te voegen element:</label>
      <input type="text" id="textID" placeholder="Nieuw element" />
   </form>

   <!-- knoppen -->
   <br>
   <a href="#">Voeg toe <strong>onderaan</strong> de lijst</a><br>
   <a href="#">Voeg toe <strong>bovenaan</strong> de lijst</a><br>
   <br>
   <a href="#">Verwijder het <strong>onderste</strong> element</a><br>
   <a href="#">Verwijder het <strong>bovenste</strong> element</a><br>
   <br>

   <!-- lijst -->
   De lijst:
   <ul id="lijstID"></ul>

</body>
</html>
```
