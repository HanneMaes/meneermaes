---
title: Browser Based Multiplayer Game
created: 2026-06-04 10:32:55 +0200
last_modified: 2026-06-04 10:46:21 +0200
---

# Database aanmaken 

Maak in **PhpMyAmdin** een nieuwe database met 1 **tabel** voor **gerbuikers**.  
Voeg **minstens 1** gebruiker toe met **gebruikersnaam & wachtwoord**.  

# Login form *(php)*

Maak een formulier met een **textfield** voor **gebruikersnaam** en **wachtwoord**.  
Wanneer de gebruiker op de knop druk kijk je of de gebruikernaam in de database zit:
- Zit de gebruikersnaam **wel** in de database: dan log je in en maak je een **sessie** aan.
- Zit de gebruikersnaam **niet** in de database: dan maak je een nieuw account.

# Basic Gameplay *(php)*

***Dit is een voorbeeld van gameplay, maar je mag uiterraard je eigen regels gebruiken.***

Je start het spel met `100 goud/cash/...`.

Je kan 3 soorten `soldaten/spaceships/...` kopen:
- **Werkers**:  
    - Verdienen: `3 goud/cash/...` per uur
    - Attack: `1`
    - Defence: `1`
- **Verdedigers**:
    - Verdienen: `1 goud/cash/...` per uur
    - Attack: `1`
    - Defence: `3`
- **Aanvallers**:
    - Verdienen `1 goud/cash/...` per uur
    - Attack: `3`
    - Defence: `1`
