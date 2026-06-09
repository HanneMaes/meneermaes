---
title: Je 1e Bot
created: 2026-06-09 10:34:47 +0200
last_modified: 2026-06-09 14:31:54 +0200
---

# Folders

**Robocode moet weten waar jouw robot staat opgeslagen.**
Elke robot krijgt een **eigen map** in een hoofdmap.

1. Maak een hoofdmap met de naam `bots-naam`.
2. Zet je robot in een eigen map binnen bots.
3. Voeg dan de map bots toe bij de instellingen, zodat Robocode je robots kan vinden: open Robocode.  
4. Ga bovenaan naar {% include ui.html ui='Config, Bot Root Directories, Add' %}  
5. Kies de map bots die je hebt gemaakt.  
6. Klik op `OK`.  

# Je Bot Instellen 

**Je robot heeft informatie nodig, zoals een naam en versie.**

Maak in de map van je robot een bestand met de naam: `naam.json`

{% include callout.html type='Belangrijk' content='
De naam van het .json-bestand moet **hetzelfde** zijn als de map van je robot.
' %}

Plak deze code in het bestand:

```json 
{
  "name": "My First Bot",
  "version": "1.0",
  "authors": [ "Jouw naam" ],
  "description": "Mijn eerste robot"
}
```

`name`, `version` en `authors` zijn verplicht.  
Zonder deze gegevens werkt je robot niet.

# Je Bot Programmeren

Maak een 2e bestand met de naam: `naam.py`

{% include callout.html type='Belangrijk' content='
De naam van het .py-bestand moet **hetzelfde** zijn als de map van je robot.
' %}

## Base Code 

Plak deze code in het bestand:

```python
from robocode_tank_royale.bot_api import Bot


class MyFirstBot(Bot):

  # Wordt uitgevoerd wanneer een nieuwe ronde start
  def run(self) -> None:

    # Herhaal zolang de robot 'leeft'
    while self.running:

      self.forward(100)
      self.turn_gun_left(360)
      self.back(100)
      self.turn_gun_left(360)

      pass


def main() -> None:
  bot = MyFirstBot()
  bot.start()


if __name__ == "__main__":
  main()
```

Met deze code blijft je robot steeds opnieuw bewegen:
1. Hij gaat 100 stappen vooruit
2. Draait zijn gun 360°
3. Gaat 100 stappen achteruit
4. Draait opnieuw 360°

**Dit herhaalt zich steeds in een lus, zodat de robot blijft bewegen.**

Zolang de code in run blijft, kan de robot blijven werken.  
Als je uit run zou gaan, stopt de robot met nieuwe acties.  

Daarom gebruik je een lus die blijft lopen zolang de robot actief is.

Als de robot moet stoppen, geeft running() automatisch False terug.  
Dan stopt de lus en eindigt de run-functie netjes.  

## Event Handlers 

Event handlers zijn “reacties” van je robot op dingen die gebeuren.
- Ze starten altijd met `on_...`
- Ze worden **automatisch** uitgevoerd als iets gebeurt

### on_scanned_bot()

Als je robot een andere robot ziet, gebeurt dit event automatisch.

```python 
from robocode_tank_royale.bot_api.events import ScannedBotEvent

class MyFirstBot(Bot):
    ...
    # Schiet met het kanon wanneer een vijand wordt gezien
    def on_scanned_bot(self, e: ScannedBotEvent) -> None:
        self.fire(1)
```

**Wat gebeurt er?**
1. Robot scant een andere robot
2. `on_scanned_bot()` wordt automatisch gestart
3. Je robot vuurt met zijn kanon

### on_hit_by_bullet()

Als je robot geraakt wordt wordt `on_hit_by_bullet()` automatisch uitgevoerd

```python 
from robocode_tank_royale.bot_api.events import HitByBulletEvent

class MyFirstBot(Bot):
    ...
    # Wordt geraakt door een kogel: draai weg van de kogel
    def on_hit_by_bullet(self, e: HitByBulletEvent) -> None:
        # Berekent uit welke richting de kogel kwam
        bearing = self.calc_bearing(e.bullet.direction)

        # Draai 90° weg van de kogel
        self.turn_right(90 - bearing)
```

**Wat gebeurt er?**
1. Je robot wordt geraakt
2. Hij berekent van welke kant de kogel kwam
3. Hij draait 90° weg van die richting
4. Zo probeert hij volgende kogels te vermijden

## Alles samenvoegen 

Hier zetten we alle onderdelen van je robot samen in één codebestand:
- start van de robot (run)
- beweging in een lus
- reageren als je een robot ziet
- reageren als je geraakt wordt

```python 
from robocode_tank_royale.bot_api.bot import Bot
from robocode_tank_royale.bot_api.events import HitByBulletEvent

class MyFirstBot(Bot):

    def run(self):
        # Blijf lopen zolang de robot actief is
        while self.running():
          # code hier ...

    # Als we een andere robot zien → schiet
    def on_scanned_bot(self, event):
        # code hier ...

    # Als we geraakt worden → draai weg van de kogel
    def on_hit_by_bullet(self, e: HitByBulletEvent):
        # code hier ...
```

# Je Bot Kleur geven

**Je kan je robot een eigen look geven door kleuren in te stellen.**

```python 
from robocode_tank_royale.bot_api import Bot, Color

class MyFirstBot(Bot):
    def run(self) -> None:

      # Kleuren instellen
      self.body_color = Color.RED
      self.turret_color = Color.BLACK
      self.radar_color = Color.CYAN

      while self.running():
```

**Wat doet dit?**
- `self.body_color`: kleur van het lichaam van je robot
- `self.turret_color`: kleur van het kanon
- `self.radar_color`: kleur van de radar
