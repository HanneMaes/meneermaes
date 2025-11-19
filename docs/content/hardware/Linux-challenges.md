---
title: Linux challenges
created: 2024-11-28T13:37:48+01:00
---

# Terminal aanpassen

1. Leer hoe je het systeem kunt **updaten** en apps kan **installeren** via `apt`.
2. Zoek uit hoe je tekstbestanden aan kan passen via `nano`.
3. Zoek uit hoe je bestanden kan openen met hun **default app**.
4. Zoek uit wat de functie van `.bashrc` is.
5. Gebruik een `alias` om een command makkelijker uit te voeren.
6. Schrijf een script om een aangepaste begroeting en de huidige systeemdatum en -tijd weer te geven wanneer je de terminal opent.
7. Installeer `screenfetch` om systeem informatie weer te geven wanneer je de terminal opent.
8. Voer `screenfetch` automatisch uit wanneer je de terminal opent.
9. Schrijf een "fortune cookie" script met willekeurige citaten of grappen en voeg dit toe aan je `.bashrc`.
10. Gebruik `cowsay` of `figlet` in je "fortune cookie" script.

# Je eigen Linux server 

## 1. Automatisatie

1. Schrijf een script dat je **belangrijkste config files en bestanden** upload naar **Google Drive** met `rclone`, zodat je een backup hebt.
2. Maak een **shutdown script** dat eerst alle belangrijkste bestanden upload naar **Google Drive**, en daarna aflsuit zodat je altijd een backup hebt van je meest recente bestanden.
3. Stel `Cron-jobs` in om **minstens 2 taken te automatiseren**, zoals systeem updates plannen of wekelijks downloads opruimen of organiseren.

## 2. Systeem monitoring en processen

1. Gebruik commands zoals `top`, `htop`, of `ps` om actieve processen te bekijken.
2. Beëindig een specifiek proces veilig met `kill` of `pkill`.

## 3. Remote connection

1. Log met een Windows-computer in op je Linux-systeem via `ssh`.
2. Kopieer bestanden van een Windows-computer naar je Linux-systeem via `SCP`.

## 4. Webservers

1. Leer hoe je een eenvoudige webserver start met `python3 -m http.server`
2. Leer hoe je een eenvoudige file-sharing server start met `python3 -m http.server 8000`.
3. Leer hoe je een lokale FTP-server opzet met `vsftpd` of `python3 -m pyftpdlib`.

## Advanced Servers

1. Zet je eigen Nextcloud (Google Drive alternatief) server op.
2. Zet je eigen Bitwarden password manager server op.
3. Zet je eigen adblock server op met Pi-hole.
4. Zet je eigen home automation server op met Home Assistant.

## 5. Media centers & gameservers

1. Bouw je Raspberry Pi om tot een retro gaming console.
2. Bouw je Raspberry Pi om tot een Media center.
3. Run een Minecraft server op je Raspberry Pi.

{% include doelen.html data='linux-challenges' %}
