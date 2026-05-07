---
title: Testing
created: 2026-04-28 08:39:54 +0200
last_modified: 2026-05-07 12:14:47 +0200
---

Een website bouwen is stap 1. Een website testen is stap 2.  
Pas dan weet je of jouw website **echt bruikbaar** is op verschillende **schermen, browsers en toestellen**.

Een website die er op jouw computer goed uitziet, werkt niet automatisch goed op andere schermen of in andere browsers.

{% include callout.html type='Belangrijk' content='
Een website hoeft niet dezelfde layout te hebben op elk toestel, maar dat de kernfunctionaliteit overal blijven werken.
' %}

In webdevelopment gebruikt men hiervoor vaak deze termen:
- **Responsive testing**  
  Testen of een website goed werkt op mobiel, tablet en desktop.
- **Cross-browser testing**  
  Testen of een website werkt in verschillende browsers en op verschillende toestellen.
- **Accessibility testing**  
  Testen of een website bruikbaar is voor zoveel mogelijk mensen, ook voor mensen met een beperking.

# Stap 1: Testen met DevTools

De snelste eerste controle doe je in de browser met de {% include btn.html btn="F12" %} **Developer Tools**.

**Wat controleer je hier?**
- Past de inhoud netjes binnen **alle schermen**?
- Moet je **horizontaal** scrollen? Dat is meestal een slecht teken.
- Blijven tekst, afbeeldingen en knoppen goed **leesbaar en aanklikbaar**?
- Werkt het menu nog **vlot** op een kleiner scherm?

**Typische fouten:**
- Tekst die te klein wordt.
- Zaken die buiten het scherm vallen.
- Knoppen die te klein zijn of te dicht bij elkaar staan.
- Een navigatiemenu dat deels verdwijnt of onbruikbaar wordt.
- Een formulier waarbij het toetsenbord op smartphone de invoervelden bedekt.

# Stap 2: Testen op echte toestellen

Een simulatie is handig, maar geen perfecte vervanging voor een **echt toestel**.

Daarom is het belangrijk om je website online te zetten en ze te testen op zo veel mogelijk verschillende **echte** smartphones, tablets en laptops.

**Test minstens dit:**
- Een smartphone in **portrait en landscape**.
- Een tablet.
- Een laptop of desktop.
- Test **alle browsers** die op het toetsel staan.

**Let extra op:**
- Laadt de site snel genoeg?
- Reageren knoppen en links goed op aanraken?
- Is tekst nog leesbaar zonder in te zoomen?
- Werkt de navigatie logisch?
- Blijft belangrijke inhoud zichtbaar wanneer het scherm draait?

{% include callout.html type='Tip' content='
Gebruik elkaars toestellen om te testen.
' %}

# Stap 3: Testen in verschillende browsers

Niet elke browser zet code om in exact dezelfde pixels op het scherm.  
Browsers ondersteunen bepaalde CSS- en JavaScript-features soms net anders.  
Daarom controleer je best of je website goed werkt in meerdere browsers en niet alleen in jouw favoriet.

**Er zijn 3 belangrijke browser engines die het web renderen:**
- Blink *(Chrome)*
- Gecko *(Firefox)*
- WebKit *(Safari)*

Zo goed als **alle moderne browsers** gebruiken onder de motorkap één van deze 3 engines. Ze hebben vooral een eigen interface (UI) ontwikkeld, maar **de echte rendering gebeurt via deze engines**.

```
Blink: Google, 2013 (fork van WebKit)
├── Chrome
├── Edge 
├── Opera
├── Brave
├── Vivaldi
└── Alle Chromium-browsers (~70% marktaandeel)

WebKit: Apple, 2003 (fork van KHTML)
├── Safari
├── alle browsers op iOS (niet alleen de officiële)
├── GNOME Web
└── Orion

Gecko: Mozilla, 1997
├── Firefox
└── Tor Browser
```

Elke engine interpreteert HTML/CSS/JavaScript **net iets anders**.  
Wat perfect werkt in Chrome breekt soms in Firefox of Safari. Door tegen alle 3 te testen, weet je zeker dat 99% van je gebruikers **je site ziet zoals bedoeld**.

> Kijk niet alleen naar **ziet het er hetzelfde uit?**, maar vooral naar **werkt het nog goed genoeg?**

# Stap 4: Accessibility testing

Accessibility betekent dat je website **bruikbaar is voor zoveel mogelijk mensen**, ook voor gebruikers met een visuele, motorische of cognitieve **beperking**.

**Wat moet je controleren?**
- **Hebben afbeeldingen een zinvolle alt-tekst?**  
  Belangrijk voor mensen die de afbeelding niet kunnen zien. Een schermlezer leest die tekst voor, zodat de inhoud en functie van de afbeelding toch duidelijk blijven.
- **Is er genoeg contrast tussen tekst en achtergrond?**  
  Zorgt ervoor dat tekst leesbaar blijft, ook voor mensen met slecht zicht of kleurenblindheid. Zonder voldoende contrast kan een site “mooi” lijken, maar in de praktijk moeilijk of vermoeiend zijn om te lezen.
- **Zijn knoppen en links duidelijk herkenbaar?**  
  Helpt iedereen om snel te zien wat klikbaar is. Als iets op een link of knop lijkt maar dat niet duidelijk is, moeten gebruikers gaan gokken, en dat verhoogt de foutkans.
- **Gebruik je semantische HTML zoals `a`, `nav`, `main` en `label` in plaats van overal `div`?**  
  Belangrijk omdat browsers en assistieve technologie dan beter begrijpen wat elk onderdeel doet. Een `div` zegt alleen “vakje”, maar een `a` zegt “dit is een link”, en dat maakt een groot verschil voor schermlezers en toetsenbordnavigatie.

{% include callout.html type='Belangrijk' content='
Toegankelijkheid gaat niet alleen over mensen met een beperking. Het maakt websites ook beter op kleine schermen, met traag internet, met een touchpad, of wanneer iemand in een moeilijke situatie snel iets moet vinden.
' %}

**Handige tools:**
- De {% include btn.html btn="F12" %} **Developer Tools** en meer specifiek:
  - [Accessibility Inspector](https://firefox-source-docs.mozilla.org/devtools-user/accessibility_inspector/-) voor **Firefox**
  - [Lighthouse](https://developer.chrome.com/docs/lighthouse) in **Chrome**.  
- [WAVE](https://wave.webaim.org/) of andere **checker-tools**.

{% include callout.html type='Belangrijk' content='
Automatische tools vinden veel fouten, maar niet alles. Handmatig testen blijft nodig.
' %}

# Extra Resources

**MDN**
- [Introduction to cross-browser testing](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Testing/Introduction)
- [Strategies for carrying out testing](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Testing/Testing_strategies)
- [Accessibility tooling and assistive technology](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/Tooling)
- [Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [Mobile accessibility](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/Mobile)

> Een goede website werkt niet alleen op jouw scherm, maar voor **echte gebruikers in echte situaties**.
