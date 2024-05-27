---
title: LaTeX
last_modified_at: 2024-05-20 14:05:53 +0200
date: 2024-05-20 14:05:53 +0200
---

![LaTeX logo](images/LaTeX-logo.svg)

> Uitgesproken als “**LAY-tek**” of “**LAH-tek**”

LaTeX is een **krachtige markup taal** *(opmaaktaal)* om **professionele text documenten** te maken *(vergelijkbaar met Microsoft Word)* dat zich richt op complexe documenten, zoals academische papers, wetenschappelijke artikelen, ...  
Het is zeer goed in het maken van complexe **wiskundige formules en symbolen**, waardoor het veel word gebruikt binnen disciplines zoals wiskunde, **informatica**, techniek en economie.

LaTeX-code kan geschreven worden in elke **teksteditor** en wordt **gecompileerd** tot een document, daardoor is het platformonafhankelijk en kan het worden gebruikt op **Linux**, **MacOS** en **Windows**.

## LaTeX vs Markdown

- **Markdown**  
	Een **simple markup taal** *(opmaaktaal)* die makkelijk te leren is, en ontworpen is voor **eenvoudige opmaak** en voornamelijk gebruikt word voor het schrijven van **webcontent en documentatie**.  
- **LaTeX**  
	Biedt veel **meer controle** over de opmaak van **complete en professionele documenten** en ondersteunt onder andere wiskundige notaties, kan automatisch bronvermeldingen opmaken, ...

# LaTeX gebruiken

De **bekendste** online LaTeX editor is Overleaf: [https://www.overleaf.com/](https://www.overleaf.com/).  
Je bestanden worden online opgeslagen, maar je moet eerst een **account maken**.

**Online LaTeX editors voor formules**

Er zijn ook online LaTeX editors gespecialiseerd in formules, voor onderstaande editors heb je **geen account** nodig:
- [https://latex.codecogs.com/eqneditor/editor.php](https://latex.codecogs.com/eqneditor/editor.php)
- [https://latexeditor.lagrida.com/](https://latexeditor.lagrida.com/)
- [https://math-editor.online/](https://math-editor.online/)
- [https://www.commontools.org/tool/latex-compiler-and-equation-writer-18](https://www.commontools.org/tool/latex-compiler-and-equation-writer-18)

# Je 1e LaTeX-document

1. Surf naar [https://www.overleaf.com/](https://www.overleaf.com/) en maak een account.
2. Klik op {% include ui.html ui='Create a new project, Blank Project' %} en geef je project een passende naam.
3. Kopieer deze code, klik rechtsboven op {% include ui.html ui='Recompile' %}, of gebruik de shortcut {% include btn.html btn='ctrl' %} {% include btn.html btn='S' %}.
	```latex
	\documentclass{article}
	\begin{document}
	Hello world!
	\end{document}
	```
4. Laten we nu wat extra informatie toevoegen.
	```latex
	\documentclass{article}
	\title{My first LaTeX document}
	\author{Meneer Maes}
	\date{Mei 2024}

	\begin{document}
	\maketitle
	Hello world!

	\end{document}
	```
	Met `\title`, `\author` en `\date` kan je extra informatie instellen en met `\maketitle` kan je kiezen waar in je document deze informatie moet komen.

	Het is handig om informatie zoals de datum en de auteur bovenaan het document in te stellen, dit maakt het gemakkelijker om belangrijke details over het document te vinden en aan te passen.
5. De volgende stap is om tekstopmaak toe te voegen.
	```latex
	Zo maak je tekst \textbf{vet (bold)}.

	Zo \underline{onderlijn} je tekst.

	En zo maak je tekst \textit{cursief (italic)}.
	```
6. Een ander zeer nuttig commando is `\emph{argument}`, waarvan het effect op zijn argument afhangt van de context. In normale tekst wordt de benadrukte tekst cursief weergegeven, maar dit gedrag wordt omgekeerd als het wordt gebruikt binnen cursief gedrukte tekst.
	```latex
	Zo ziet \emph{het emph commando} eruit in gewone tekst.

	\textit{Zo ziet \emph{het emp commando} eruit in cursieve tekst.}

	\textbf{Zo ziet \emph{het emp commando} eruit in vet gedrukt tekst.}
	```
7. Verander `\documentclass` van `article` naar `beamer` en bekijk wat het effect is.
	```latex
	\documentclas{beamer}
	```
8. Om je document te downloaden klik je op het {% include btn.html btn='Download' %} icoontje naast {% include btn.html btn='Compile' %}.  
	![download](images/download.png){: width='300px' }

## Document-type

Er zijn meerdere document-types beschikbaar in LaTeX. Elke klasse biedt verschillende structuren, lay-outs en opmaakopties die zijn afgestemd op specifieke soorten documenten.

- `article`: Deze klasse is bedoeld voor het schrijven van **korte documenten** *(artikelen, essays, ...)*. Het biedt een eenvoudige structuur met secties en subsections, maar zonder hoofdstukken.
- `book`: Deze klasse is ontworpen voor **boeken**. Het biedt hoofdstukken, secties, subsecties en andere hiërarchische structuren die geschikt zijn voor langere documenten.
- `beamer`: Deze klasse is voor **presentaties**. Het biedt functies voor het maken van dia's met verschillende lay-outs en stijlen.
- `slides`: Deze klasse is voor het maken van **handouts** die vaak bij **presentaties** met de beamer documentklasse horen. 

## Afbeeldingen

1. Om afbeeldingen te gebruiken moeten we eerst enkele **libraries** importeren, **deze moeten onder `\documentclass` staan**.
	```latex
	\documentclass{article}
	\usepackage{graphicx} %LaTeX package to import graphics
	\graphicspath{{images/}} %configuring the graphicx package
	```

Positionering
```latex
\begin{figure}
    \centering
    \includegraphics[width=0.5\linewidth]{LaTeX-logo.jpg}
    \caption{Enter Caption}
    \label{fig:enter-label}
\end{figure}
```

LaTeX probeert figuren en tabellen op een 'goede' plaats te zetten, wat soms resulteert in het verplaatsen van deze elementen naar de volgende pagina of het einde van het document, vooral als er niet genoeg ruimte is op de huidige pagina.

Om de afbeelding te forceren op de plaats waar je deze wilt hebben, kun je een positieparameter toevoegen aan de figure-omgeving. De meest gebruikte opties zijn:

h voor 'here' (hier)
t voor 'top' (bovenkant van de pagina)
b voor 'bottom' (onderkant van de pagina)
p voor 'page' (apart figuren-pagina)
Je kunt ook meerdere opties combineren en LaTeX laten proberen ze in die volgorde te gebruiken, bijvoorbeeld [htbp].

```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.5\linewidth]{LaTeX-logo.jpg}
    \caption{Enter Caption}
    \label{fig:enter-label}
\end{figure}
```

# Je 1e LaTeX-formule

```latex
\[ a^2 + b^2 = c^2 \]
```

```latex
\[
\int_{a}^{b} x^2 dx
\]
```

# Templates

[https://www.overleaf.com/latex/templates](https://www.overleaf.com/latex/templates)

---

Guides
- [https://chatgpt.com/c/f8f74c72-a67a-41fe-9401-1360cad41b51](https://chatgpt.com/c/f8f74c72-a67a-41fe-9401-1360cad41b51)
- [https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes](https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes)

# Opdracht

{% include punten.html data='LaTeX' %}

## Optie 1: Beschrijving van een wiskundig of technologisch concept

Maak een LaTeX-document over een wiskundig of technologisch concept.
Geef een korte beschrijving van het concept en voeg een LaTeX-formule toe.

Technologische concepten:
--> Nog voorbeelden laten zien van hoe de formules eruit moeten zien, de leerlingen zelf laten zoeken wat het concept betekend en waarom het balangrijk is.
- Leg uit hoe de frequentie van een golf wordt berekend en wat de relatie is tussen frequentie, golflengte en snelheid.
- Beschrijf de wet van Snellius, die de breking van licht aan de grens tussen twee media beschrijft.
- Leg uit hoe de capaciteit van een condensator wordt berekend.
- Leg uit hoe je de totale weerstand berekent voor weerstanden in serie en parallel.
- **De Basis van de Spanningsdeler**: Leg uit hoe een spanningsdeler werkt en hoe je de uitgangsspanning berekent.

Wiskundige concepten:
- **Pythagoras**: beschrijving van de stelling van Pythagoras en hoe deze formule wordt gebruikt om de lengte van de zijde van een rechthoekige driehoek te berekenen.
- Beschrijf het verband tussen twee numerieke grootheden in een dataset met behulp van een spreidingsdiagram.
- Beschrijf het telproblemen zonder herhaling.
- Kansen bepalen met behulp van kruistabellen.
- het verband tussen de grafiek van een algemene sinusfunctie f(x)= a·sin[b(x-c)] en haar kenmerken: nulwaarden, tekenverloop, stijgen/dalen, extrema, periode, amplitude, faseverschuiving.
- vergelijkingen op van de vorm sin(ax+b)=c
- Het oplossen tweedegraadsvergelijkingen.
- kenmerken van tweedegraadsfuncties: nulwaarden, tekenverloop, stijgen/dalen, extremum en symmetrie ten opzichte van een verticale rechte.
- exponentiële vergelijkingen van de vorm ax=c
- interpreteren de afgeleide als limiet van een differentiequotiënt en als richtingscoëfficiënt van de raaklijn aan de grafiek.
Beheersingsniveau

### Puntenverdeling:
- Correct gebruik van LaTeX (Netheid en organisatie van het document, goed gestructureerde opmaak, ...): 4 punten
- Inclusie van LaTeX-formule: 4 punten
- Nauwkeurige beschrijving van het wiskundige concept: 2 punten

## Optie 2:

Maak een LaTeX-document dat de verschillen beschrijft tussen het schrijven van formules in Microsoft Word en LaTeX.  
Voeg voorbeelden toe van hoe je in elk systeem een wiskundige formule kan invoegen.
Beschrijf de verschillen en gelijkenissen als ook de voordelen van elk systeem.

### Puntenverdeling:
- Correct gebruik van LaTeX (Netheid en organisatie van het document, goed gestructureerde opmaak, ...): 4 punten
- Inclusie van LaTeX-formule: 2 punten
- Inclusie van Word-formule: 2 punten
- Nauwkeurige beschrijving van de verschillen, gelijkenissen en voordelen: 2 punten

### Voorbeelden
- links naar pagina's met voorbeelden