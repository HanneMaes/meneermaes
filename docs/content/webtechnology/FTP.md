---
title: FTP
last_modified_at: 2024-05-21 15:07:48 +0200
date: 2024-05-21 15:07:48 +0200
---

> Staat voor **"File Transfer Protocol"**.

Het is een standaard netwerkprotocol dat wordt gebruikt om bestanden van de ene computer naar de andere over te dragen via het internet. **FTP maakt het mogelijk om bestanden te beheren op een server**.

# FTP en SFTP

**SFTP (Secure File Transfer Protocol)** is een veiliger alternatief voor FTP omdat het gebruikmaakt van **encryptie** om de gegevens te beschermen **tijdens de overdracht**.
- **FTP** verzendt gegevens in **gewone tekst**, wat betekent dat de gegevens, inclusief gebruikersnamen en wachtwoorden, niet versleuteld zijn. Dit maakt FTP kwetsbaar voor onderschepping en afluisteren door kwaadwillenden.
- **SFTP** maakt gebruik van SSH (Secure Shell) om een beveiligde verbinding tot stand te brengen. **Alle gegevens die worden verzonden**, inclusief inloggegevens en bestanden, zijn **versleuteld**.

# Itbusleyden.be

We zullen werken met onze eigen webserver. Iedereen krijgt zijn persoonlijke webpagina op deze server waarop je webcontent kan publiceren. Deze pagina's zullen toegankelijk zijn via individuele URL's, zoals bijvoorbeeld [http://hannemaes.itbusleyden.be/](http://hannemaes.itbusleyden.be/).

# CrossFTP

![CrossFTP Logo](images/crossftp-logo.png){: width='100px' }{: .wrap }
Er zijn veel FTP-programma's beschikbaar, en een van de meest gebruikte *(op Windows)* is [CrossFTP](https://www.crossftp.com). Dit programma is cross-platform, wat betekent dat het werkt op Linux, MacOS en Windows. Hoewel er een betaalde versie beschikbaar is, biedt de gratis versie alle functionaliteiten die we voor ons gebruik nodig hebben.

## Nieuwe verbinding aanmaken

1. {% include ui.html ui='Bestand, Verbinden' %}
2. Maak een verbinding met deze gegevens:
	{% include ui.html ui='Protocol: FTP' %}
	{% include ui.html ui='Host: ' %}

## Bestanden overzetten

![CrossFTP Window](images/crossftp-screenshot.png)

## Bestaande verbinding aanpassen

1. {% include ui.html ui='Sites, Site beheer' %}