---
title: LaTeX Documenten
last_modified: 2025-03-31 10:05:03 +0200
created: 2024-05-27 21:29:48 +0200
---

![](images/overleaf.svg){: .wrap }
De **bekendste** online LaTeX editor is [https://www.overleaf.com/](https://www.overleaf.com/).  
Je bestanden worden **online opgeslagen**, maar je moet eerst een **account maken**.

# Basis syntax

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
   Het is handig om informatie zoals de datum en de auteur bovenaan het document in te stellen, dit maakt het gemakkelijker om belangrijke details over het document snel te vinden en aan te passen.

# Tekst opmaak

- Op deze manier maak je tekst **vet**, **cursief** en **onderlijnd**.

  ```latex
  Zo maak je tekst \textbf{vet (bold)}.

  Zo \underline{onderlijn} je tekst.

  En zo maak je tekst \textit{cursief (italic)}.
  ```

- Een ander zeer nuttig commando is `\emph{argument}`, waarvan het effect op zijn argument afhangt van de context. In normale tekst wordt de benadrukte tekst cursief weergegeven, maar dit gedrag wordt omgekeerd als het wordt gebruikt binnen cursief gedrukte tekst.

  ```latex
  Zo ziet \emph{het emph commando} eruit in gewone tekst.

  \textit{Zo ziet \emph{het emp commando} eruit in cursieve tekst.}

  \textbf{Zo ziet \emph{het emp commando} eruit in vet gedrukt tekst.}
  ```

- Hieronder zie je hoe je een **line break** maakt.
  ```latex
  Je kan een lege lijn maken door 2 backslashes te gebruiken\\
  De lijn hierboven heeft 1 line break gekregen.
  \\
  \\
  Hierboven gebruik ik 2 maal een line break om een lege lijn te krijgen.
  ```
  Het commando `\\` kan je vergelijken met `<br>` in HTML.

# Afbeeldingen

1. Als eerste importeren we enkele **libraries**, **deze moeten onder `\documentclass` staan**.
   ```latex
   {% raw %}
   \usepackage{graphicx} %needed for images: LaTeX package to import graphics
   \graphicspath{{images/}} %needed for images: configuring the graphicx package
   {% endraw %}
   ```
2. Daarna uploaden we de afbeelding via de **Insert Figure** knop bovenaan, de code voor de afbeelding zal automatisch toegevoegd worden.  
   ![](images/image-btn.png){: .square }

```latex
\begin{figure}
	\centering
	\includegraphics[width=0.5\linewidth]{download.png}
	\caption{Enter Caption}
	\label{fig:enter-label}
\end{figure}
```

- `\centering`: De afbeelding wordt in het **midden van de pagina** wordt geplaatst.
- `[width=0.5\linewidth]`: Deze optie stelt de **breedte van de afbeelding** in op de helft van de breedte van de omringende tekst. Je kunt ook andere eenheden gebruiken, zoals cm, in of een relatieve waarde zoals 0.5\textwidth.
- `\caption{Enter Caption}`: Dit voegt een **bijschrift** toe aan de afbeelding. Het bijschrift verschijnt onder de afbeelding.
- `\label{fig:enter-label}`: Deze opdracht definieert een label voor de figuur, waarmee je later in de tekst naar deze figuur kunt **verwijzen**. Door `\ref{fig:enter-label}` ergens anders in je document te plaatsen, kun je het figuurnummer oproepen.

3. LaTeX probeert figuren en tabellen op een 'goede' plaats te zetten, wat soms resulteert in het verplaatsen van deze elementen naar de volgende pagina of het einde van het document, vooral als er niet genoeg ruimte is op de huidige pagina.
   Om de afbeelding te forceren op de plaats waar je deze wilt hebben, kun je een **positieparameter** toevoegen. De meest gebruikte opties zijn:

- `h` voor **here** _(hier)_
- `t` voor **top** _(bovenkant van de pagina)_
- `b` voor **bottom** _(onderkant van de pagina)_
- `p` voor **page** _(apart figuren-pagina)_

```latex
\begin{figure}[h]
	\centering
	\includegraphics[width=0.5\linewidth]{LaTeX-logo.jpg}
	\caption{Enter Caption}
	\label{fig:enter-label}
\end{figure}
```

# Document types

Verander `\documentclass` van `article` naar `beamer` en bekijk wat het effect is.

```latex
\documentclas{beamer}
```

- `article`: Deze klasse is bedoeld voor het schrijven van **korte documenten** _(artikelen, essays, ...)_. Het biedt een eenvoudige structuur met secties en subsecties, maar zonder hoofdstukken.
- `book`: Deze klasse is ontworpen voor **boeken**. Het biedt hoofdstukken, secties, subsecties en andere hiërarchische structuren die geschikt zijn voor langere documenten.
- `beamer`: Deze klasse is voor **presentaties**. Het biedt functies voor het maken van dia's met verschillende lay-outs en stijlen.
- `slides`: Deze klasse is voor het maken van **handouts** die vaak bij **presentaties** met de beamer documentklasse horen.

Er zijn meerdere document-types beschikbaar in LaTeX. Elke klasse biedt verschillende structuren, lay-outs en opmaakopties die zijn afgestemd op specifieke soorten documenten.

# Downloaden

Om je document te downloaden klik je op het {% include btn.html btn='Download' %} icoontje naast {% include btn.html btn='Compile' %}.

![download](images/download.png){: width='300px' }
