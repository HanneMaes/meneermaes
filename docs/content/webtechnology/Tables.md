---
title: Tables
created: 2026-09-23 10:02:17 +0200
last_modified: 2026-09-23 14:56:36 +0200
---

Een tabel gebruik je om gegevens in rijen en kolommen weer te geven.

{% include browser.html img='images/table-base.png' %}  

# Table Basics

Een tabel bestaat uit **3 belangrijke onderdelen:**

- `<table>`: de volledige tabel
- `<tr>`: een rij (table row)
- `<td>`: een cel (table data)

```html
<table border="1">
  <!-- 1e rij -->
  <tr>
    <td>Cell 1</td>
    <td>Cell 2</td>
  </tr>

  <!-- 2e rij -->
  <tr>
    <td>Cell 3</td>
    <td>Cell 4</td>
  </tr>

  <!-- 3e rij -->
  <tr>
    <td>Cell 5</td>
    <td>Cell 6</td>
  </tr>
</table>
```

Je kunt de HTML van buiten naar binnen lezen:
1. `<table border="1">`: start van de tabel
2. `<tr>`: start van een rij 
3. `<td>Cell 1</td>`: de 1e cell in de rij 
4. `<td>Cell 2</td>`: de 2e cell in de rij 
5. `</tr>`: het einde van de rij 
6. `</table>`: het einde van de tabel

Je kan het zien als:
```
TABLE <table>
│
├── ROW <tr>
│   ├── CELL <td>
│   └── CELL <td>
│
├── ROW <tr>
│   ├── CELL <td>
│   └── CELL <td>
│
└── ROW <tr>
    ├── CELL <td>
    └── CELL <td>
```

## Border 

`border="1"` zorgt ervoor dat je randen rond de tabel en cellen ziet:
{% include browser.html img='images/table-base.png' %}  

**Zonder** het border attribute krijg je geen randen te zien:
{% include browser.html img='images/table-no-border.png' %}  

> Ik raad aan om tijdens het opbouwen van een tabel steeds een border te gebruiken. Zo kun je duidelijk zien hoe de rijen en cellen van je tabel worden opgebouwd.

## Header

Vaak heeft een tabel bovenaan een header. Die vertelt wat de gegevens in de kolommen betekenen.

Daarvoor gebruik je `<th>`, dit betekent **table header**.

{% include browser.html img='images/table-header.png' %}  

```html
<table border="1">
  <tr>
    <th>Naam</th>
    <th>Vak</th>
  </tr>

  <tr>
    <td>Maes</td>
    <td>Webtechnology</td>
  </tr>

  <tr>
    <td>Vermeulen</td>
    <td>Software Development</td>
  </tr>
</table>
```

# Oefening

## Basis 

Maak deze tabel met 2 kolommen en 4 rijen:  
{% include browser.html img='images/tables-oef-1.png' %}

Voeg een header toe:  
{% include browser.html img='images/tables-oef-2.png' %}

Breid de tabel uit met een derde kolom:  
{% include browser.html img='images/tables-oef-3.png' %}

Nu krijg je een nog grotere dataset:
{% include browser.html img='images/tables-oef-4.png' %} 

## Uitbreiding

Werk verder aan dezelfde table en gebruik `colspan` om een **rij over meerdere kolommen te laten lopen**.

```html 
<th colspan="4">Internet Hall of Fame</th>
```

{% include browser.html img='images/tables-oef-5.png' %} 

Zoek zelfstandig uit hoe je `rowspan` kunt gebruiken om een **cel over meerdere rijen te laten lopen**, zoals ik hieronder bij de **cell internet** gedaan heb.

{% include browser.html img='images/tables-oef-6.png' %}

## Table Puzzles

Maak deze tables **exact** na

**De Halve Piramide:**
{% include browser.html img='images/tables-puzzle-1.png' %} 

**De Brug:**
{% include browser.html img='images/tables-puzzle-2.png' %} 

**De Toren:**
{% include browser.html img='images/tables-puzzle-3.png' %} 

**De Trap:**
{% include browser.html img='images/tables-puzzle-4.png' %} 

**De Hele Piramide:**
{% include browser.html img='images/tables-puzzle-5.png' %}

# Overzicht

| Element             | Betekenis    | Gebruik                                          |
| ------------------- | ------------ | ------------------------------------------------ |
| `<table>`           | Table        | De volledige tabel                               |
| `<tr>`              | Table Row    | Een rij in de tabel                              |
| `<td>`              | Table Data   | Een cel met gegevens                             |
| `<th>`              | Table Header | Een header die de gegevens benoemt               |

| Attribuut           | Betekenis    | Gebruik                                          |
| ------------------- | ------------ | ------------------------------------------------ |
| `border="1"`        | Border       | Geeft een zichtbare rand rond de tabel en cellen |
| `colspan="2"`       | Column Span  | Laat een cel over meerdere kolommen lopen        |
| `rowspan="2"`       | Row Span     | Laat een cel over meerdere rijen lopen           |

{% include callout.html type='Element & Attribuut' content='
Een **element** vertelt de browser **wat iets is**.  
Een **attribuut** geeft **extra informatie** over een element.
' %}
