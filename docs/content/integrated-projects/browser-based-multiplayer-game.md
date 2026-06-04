---
title: Browser Based Multiplayer Game
created: 2026-06-04 10:32:55 +0200
last_modified: 2026-06-04 12:04:14 +0200
---

# Database aanmaken 

Maak in **PhpMyAmdin** een nieuwe database met 1 **tabel** voor **gerbuikers**.  
Voeg **minstens 1** gebruiker toe met **gebruikersnaam & wachtwoord**.  

# Login form *(PHP)*

Maak een formulier met een **textfield** voor **gebruikersnaam** en **wachtwoord**.  
Wanneer de gebruiker op de knop druk kijk je of de gebruikernaam in de database zit:
- Zit de gebruikersnaam **wel** in de database: dan log je in en maak je een **sessie** aan.
- Zit de gebruikersnaam **niet** in de database: dan maak je een nieuw account.

# Basic Gameplay *(PHP)*

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
