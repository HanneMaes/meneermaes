---
title: Zelf Aan De Slag Met Een Besturingssysteem
last_modified_at: 2024-10-23 16:41:02 +0200
date: 2024-10-23 15:39:25 +0200
---

In dit hoofdstuk gaan we op zoek naar besturingssystemen (OS) die passen bij specifieke projecten.  
Je zal praktische ervaring opdoen door het gekozen besturingssysteem (OS) te installeren in een virtuele omgeving.

# Hoe een nieuw OS installeren?

{% include toggle.html title="Dual Boot" content="
Dual boot is een configuratie waarbij **twee verschillende besturingssystemen op één computer** zijn geïnstalleerd, zodat je bij het opstarten kunt kiezen welk besturingssysteem je wilt gebruiken.

Het wordt vaak gebruikt om een nieuw besturingssysteem te **leren of testen**. Je kunt het nieuwe OS naast je bestaande systeem installeren en gebruiken om ermee vertrouwd te raken. Als je tevreden bent met het nieuwe besturingssysteem, kun je ervoor kiezen om het oude OS van de computer te verwijderen en alleen het nieuwe te behouden. Zo heb je de flexibiliteit om een nieuwe omgeving uit te proberen zonder meteen je huidige systeem op te geven.

**Voordelen**{: .goodText }
- Volledige toegang tot hardware
- Optimale performance
- Beste van twee werelden

**Nadelen**{: .badText }
- Complexe setup
- Moet steeds herstarten wanneer je van OS wil veranderen
- Elk OS heeft zijn eigen deel van de de harde schijf
" %}

{% include toggle.html title="Live USB" content="
Je installeert het OS op een USB-stick, en start het OS op vanaf deze USB-stick. Je gebruikt de hardware van de computer, maar het OS dat op de USB-stick staan.

Om een OS op een computer te installeren, werk je meestal met een live USB. Deze geeft je de optie om het besturingssysteem eerst te testen zonder iets aan je huidige installatie te veranderen en vervolgens het OS te installeren als je tevreden bent.

Er zijn **2 soorten** Live USB-sticks:
- **Tijdelijke opslag:** nieuwe data verdwijnt zodra je de computer uitzet.
- **Persistent opslag:** sommige Live USB's kun je configureren met een 'persistent storage', dit reserveert een deel van de USB-stick voor permanente opslag. Hiermee kun je veranderingen en bestanden bewaren, zelfs na herstart

**Voordelen**{: .goodText }
- Geen wijzigingen aan de computers
- Draagbaar systeem: eens geïnstalleerd op de USB-stick werkt het op alle computers
- Ideaal voor testen en reparatie
- Meestal heb je de optie om het OS te installeren op je computer na het eerst te kunnen testen

**Nadelen**{: .badText }
- Langzamer dan geïnstalleerd systeem
- Geen of beperkte opslagruimte
" %}

{% include toggle.html title="Virtuele Machine (VM)" content="
Een applicatie dat je kan installeren op je computer, die een computer simuleert.  
Het bekendste voorbeeld hier van is **VirtualBox**.

**Voordelen**{: .goodText }
- Veilig experimenteren zonder risico voor hoofdsysteem
- Meerdere OS'en tegelijk kunnen draaien
- **Ideaal voor testen en leren**

**Nadelen**{: .badText }
- Minder goede performance dan native installatie
- Beperkte toegang tot hardware
" %}
