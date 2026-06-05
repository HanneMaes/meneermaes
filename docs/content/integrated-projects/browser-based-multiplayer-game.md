---
title: Browser Based Multiplayer Game
created: 2026-06-04 10:32:55 +0200
last_modified: 2026-06-05 14:44:53 +0200
---

# Database aanmaken 

Maak in **PhpMyAmdin** een nieuwe database met 1 **tabel** voor **gerbuikers**.  
Voeg **minstens 1** gebruiker toe met **gebruikersnaam & wachtwoord**.  

# Login form *(PHP)*

Maak een formulier met een **textfield** voor **gebruikersnaam** en **wachtwoord**.  
Wanneer de gebruiker op de knop druk kijk je of de gebruikernaam in de database zit:
- Zit de gebruikersnaam **wel** in de database: dan log je in en maak je een **sessie** aan.
- Zit de gebruikersnaam **niet** in de database: dan maak je een nieuw account.

# Gameplay

Je kan deze zaken toevoegen aan je game in een **volgorde naar keuze**, kijk welke leerstof je nog niet helemaal beheers en probeer eerst deze zaken toe te voegen, **zo zal je het snelste leren**.

{% include callout.html type='Tip' content='
Dit is een voorbeeld van gameplay, maar je mag uiterraard je eigen regels gebruiken.
' %}

## Resource management *(PHP)*

1. Je start het spel met `100 goud/cash/...`.
2. Je kan 3 soorten `soldaten/spaceships/...` kopen:
- **Werkers**:  
    Verdienen: `3 goud/cash/...` per uur  
    Attack: `1`  
    Defence: `1`  
- **Verdedigers**:  
    Verdienen: `1 goud/cash/...` per uur  
    Attack: `1`  
    Defence: `3`  
- **Aanvallers**:  
    Verdienen `1 goud/cash/...` per uur  
    Attack: `3`  
    Defence: `1`  
3. `Goud/cash/...` bij verdienen:
  1. Elke keer dat je op de pagina komt haal je uit de database het tijdstip van de vorige keer dat je op de pagina kwam.
  2. Bereken hoeveel tijd ver streken is en hoeveel `goud/cash/...` je in die tijd verdient hebt, update je database.
  3. Update het tijdstip met de tijd van nu.

## Gevechten met randomness (PHP of JS)

Spelers kunnen andere spelers aanvallen.
Bij een gevecht is er steeds een stukje [randomness](../webtechnology/Random-story-generator-deel-1) zodat de sterkste speler niet altijd automatisch wint.

**Voorbeeld:**
1. Elke speler heeft een totale attack en defence score.
2. Voeg een random bonus toe tussen.
3. Vergelijk daarna beide scores.

**Mogelijke uitbreidingen:**
- Critical hits
- Missed attacks
- Lucky defence bonus
- Verschillende soorten aanvallen
- Cooldown timer tussen gevechten

## World Map *(PHP & CSS)*

Geef elke speler *(bij het aanmaken van hun account)* random coördinaten.  
Maak een **World Map** en plaats de naam of het icoontje van elke speler op de juiste plek op de kaart.
1. Maak een **lege div** met de **afbeelding als achtergrond**.
2. Plaats de spelers op de map door gebruik te maken van **CSS** [Display & Position](../webtechnology/Display-en-position).

## User Settings in LocalStorage *(JS)*

Maak een **menu met settings** die de user kan aanpassen en sla dit op in [LocalStorage](../webtechnology/localStorage)  
Denk hierbij aan:
- Dark/light mode 
- Lettertype
- ...

## Sharable Profile Page *(JS)*

Maak een profile page die elke speler kan customizen en sharen, **sla alle settings op in de URL** via [Url Query Parameters](../webtechnology/URL-query-parameters) zodat spelers **hun profiel kunnen delen met hun eigen customizations.  
Denk hierbij aan customizations zoals: 
- Dark/light mode 
- Lettertype
- Background color 
- ...

### Sharable Profile Page Shop *(PHP)*

Voeg een shop toe waarbij spelers zaken kunnen kopen om hun **sharable profile page** te **pimpen**.  
Denk hierbij aan zaken zoals:
- Gouden border rond hun profile pic
- Custom background image
- Geanimeerde background
- ...

## Battle Log met arrays *(JS)*

Hou tijdens het spelen een battle log bij in een [JavaScript array](https://www.meneermaes.be/content/webtechnology/Arrays).

**Voorbeeld:**
```js
let battleLog = [];

battleLog.push("Je viel Player123 aan");
battleLog.push("Critical hit!");
battleLog.push("Je won 50 goud");
```

Toon daarna alle berichten op het scherm met een loop.

**Mogelijke uitbreidingen:**
- Maximum 10 berichten bewaren
- Tijdstip toevoegen
- Verschillende kleuren voor wins/losses
- Opslaan in LocalStorage
- Animated notifications

## Notifications systeem *(JS)*

Maak een notificatie systeem met [JavaScript array](https://www.meneermaes.be/content/webtechnology/Arrays).

**Voorbeelden van meldingen:**
- "Je goud werd verzameld"
- "Nieuwe aanval beschikbaar"
- "Je werd aangevallen"
- "Achievement unlocked"

**Mogelijke uitbreidingen:**
- Meldingen automatisch laten verdwijnen
- Klikbare notificaties
- Geluidseffecten
- Mobiele popup meldingen

## Selected Troops systeem *(JS)*

Gebruik een [JavaScript array](https://www.meneermaes.be/content/webtechnology/Arrays) om bij te houden welke troepen geselecteerd zijn voor een aanval.

**Voorbeeld:**

```js
let selectedTroops = [];

selectedTroops.push("Aanvaller");
selectedTroops.push("Verdediger");
```

**Mogelijke ujitbreidingen:**
- Troepen deselecteren
- Maximum aantal troepen
- Live totaal attack/defence tonen

# Mobile Friendly *(CSS)*

Zorg ervoor dat het spel **vlot en overwichtelijk** werkt op **smartphone of tablet** zodat ze het en altijd en overal kunnen spelen.

**Denk hierbij aan:**
- Grote knoppen voor touchscreens
- [Responsive layout met media queries](../webtechnology/Responsive-design)
- [Een menu dat goed werkt op mobiel](../webtechnology/Responsive-design-met-JavaScript)

**Mogelijke uitbreidingen:**
- Bottom navigation zoals in echte mobile games
- Swipe menu
- Fullscreen mode
- Push-achtige meldingen in de browser

# Hosting op Raspberry Pi *(Linux)*

Om je browser game ook **van buiten je thuisnetwerk** speelbaar te maken, kan je een [Raspberry Pi](../flex/raspberrypi-als-server) gebruiken als [Linux server](../flex/bash).  
De Raspberry Pi draait dan je PHP + database + webserver.

# Extra ideeën
- Leaderboard met rijkste/sterkste spelers
- Clan/guild systeem
- Dagelijkse rewards
- Achievement systeem
- Chat tussen spelers
- Inventory systeem
- Trading tussen spelers
- Fog of war
- Login streak rewards
- Sound effects & muziek
- Anti-spam attack cooldown
