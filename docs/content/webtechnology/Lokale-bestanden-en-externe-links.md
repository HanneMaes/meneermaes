---
title: Lokale bestanden & externe links
last_modified_at: 2024-09-20 15:43:11 +0200
date: 2024-09-20 15:18:33 +0200
---

# Externe Links

Externe links verwijzen naar media (afbeeldingen, video's, ...) die **elders op internet zijn opgeslagen**.

```html 
<img src="https://example.com/foto.jpg">
```

**Voordelen:**
- Bespaart opslagruimte in het project.

**Nadelen:**
- Mogelijk tragere laadtijden.
- Risico op onbruikbare links bij verwijdering van de bron.

# Lokale Bestanden

Lokale media zijn bestanden die direct in de **projectmap zijn opgeslagen**.

![](images/local-image.png){: width='500px' }

```html 
<img src="images/foto.jpg">
```

**Voordelen:**
- Snellere laadtijden
- Onafhankelijkheid van externe servers.
- Offline beschikbaarheid.

**Nadelen:**
- Grotere projectomvang.
- Meer opslagruimte vereist op hosting.

# Organisatie van lokale bestanden

Bij het uploaden of delen van een website is het belangrijk om lokale **mediabestanden correct mee te sturen**, anders zullen deze niet meer werken op je website.

Het is belangrijk de **locatie van het bestand** correct te noteren.

## De afbeelding in de map media.

![](images/local-image.png){: width='500px' }
```html 
<img src="images/image.jpg">
```

## De afbeelding in dezelfde map als het .html bestand.

![](images/local-image2.png){: width='500px' }
```html 
<img src="image.jpg">
```
