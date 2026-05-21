---
title: Url Query Parameters
created: 2026-04-28 09:08:56 +0200
last_modified: 2026-05-21 12:33:10 +0200
---

# Wat zijn Query Parameters
Query parameters zijn **gegevens** die je meegeeft in een **URL**.  
Ze komen achter een vraagteken `?` en bestaan uit **key–value pairs**.

`index.html?mode=dark`  
`index.html?mode=dark&theme=tokyoNight`
- `?` start de parameters
- `=` koppelt sleutel en waarde
- `&` scheidt meerdere parameters

Deze parameters kan je ophalen via JavaScript:
```javascript
const params = new URLSearchParams(window.location.search); // Maak een variabelen die parameters uit de URL kan lezen
let mode = params.get("mode"); // haal "mode" uit de URL
let themeName = params.get("theme"); // haal "theme" uit de URL
```

{% include callout.html type='tip' content='
Query parameters zijn zichtbaar in de URL. Gebruik ze dus niet voor wachtwoorden of gevoelige gegevens.
' %}

# Query parameters toevoegen

Er zijn twee veelgebruikte manieren om query parameters te gebruiken.

## 1. Rechtstreeks in een link (HTML)

De eenvoudigste manier is parameters meteen in een hyperlink zetten.

```html
<a href="index.html?mode=dark">Activate Dark Mode</a>
```

Dit gebruik je wanneer je naar een andere pagina gaat.

## 2. De URL live aanpassen met JavaScript

Je kunt ook de URL wijzigen **zonder de pagina opnieuw te laden**.

```javascript
const url = new URL(window.location); // Maak een variabelen van de URL
url.searchParams.set("mode", "dark"); // Zet of overschrijft de query parameter "mode" met de waarde "dark"
history.replaceState({}, "", url); // Vervangt de huidige URL in de adresbalk zonder de pagina te herladen zonder een nieuwe stap toe te voegen aan de browsergeschiedenis
```

Nieuwe URL: `index.html?mode=dark`

De pagina **herlaadt niet**, maar de URL is wel aangepast.

Gebruik live aanpassen wanneer:
- De URL moet meeveranderen terwijl de gebruiker zaken aanpast
- Je state wilt bewaren zonder refresh
- Filters onmiddellijk veranderen
- Je een single page application (SPA) maakt

Voorbeelden:
- Zoekfilters live aanpassen
- Tab wisselen
- Sorteren zonder herladen
- Interactieve dashboards

# Waarom gebruiken

Soms is het handig om gegevens niet in localStorage of een database op te slaan, maar rechtstreeks in de URL:
- **Deelbare links:**  
  Als je deze URL **doorstuurt**, krijgt iemand anders exact dezelfde parameters.  
  Met localStorage werkt dat niet, want die gegevens staan enkel op jouw toestel.
- **Deep linking:**  
  Je kan rechtstreeks linken naar een specifieke toestand van een applicatie, bijvoorbeeld een bepaald filter, tabblad of zoekresultaat.  
  Je kan deze toestand ook als **bookmark opslaan**. Dat is handig wanneer je meerdere verschillende toestanden van dezelfde applicatie snel opnieuw wilt openen.
- **State blijft behouden bij vernieuwen:**  
  Als je de pagina herlaadt, blijven de parameters bestaan
- **Geen opslag nodig:**  
  Alles zit gewoon in de URL.

**Gebruik URL parameters wanneer de gebruiker mag kunnen zeggen:**

> Ik wil deze exacte pagina-toestand kunnen bookmarken of delen

## LocalStorage

Gebruik liever localStorage voor gegevens die **persoonlijk** zijn en **niet gedeeld** moeten worden:
- Thema voorkeur (dark mode)
- Taalvoorkeur
- Sidebar open/dicht
- Laatst gebruikte instellingen

Waarom?
- Blijft lokaal bewaard
- URL blijft netjes

**Gebruik localStorage wanneer je zegt:**

> Dit is een persoonlijke voorkeur

## Database

Gebruik een database voor gegevens die permanent of gedeeld moeten worden:
- Gebruikersaccounts
- Favorieten
- Winkelwagens
- Posts of comments

**Gebruik een database wanneer je zegt:**

> Dit moet permanent opgeslagen worden

# Opdracht 1: Themable website 

Maak een website waarbij je via een menu het thema volledig kan aanpassen.  
Zorg ervoor dat alle installingen opgeslagen worden in de URL, zodat je designs gedeeld kunnen worden.  
Denk bijvoorbeeld aan:
- Mode: dark, light 
- Colors: colorful, muted, black and white, flashy 
- Background: color, image, animated 
- ...
