---
title: Linux challenges
date: 2024-11-28T13:37:48+01:00
---

# Terminal aanpassen

1. Leer hoe je het systeem kunt updaten en apps kan installeren via `apt`.
2. Installeer `screenfetch` om systeem informatie weer te geven wanneer je de terminal opent.
3. Zoek uit wat de functie van `.bashrc` is.
4. Zoek uit hoe je tekstbestanden aan kan passen via `nano` of `vim`.
5. Schrijf een script om een aangepaste begroeting en de huidige systeemdatum en -tijd weer te geven wanneer je de terminal opent.
6. Gebruik een `alias` om het script makkelijker uit te voeren.
7. Schrijf een "fortune cookie" script met willekeurige citaten of grappen en voeg dit toe aan je `.bashrc`.
8. Gebruik `cowsay` of `figlet` in je "fortune cookie" script.

# Automatisatie

1. Schrijf een script dat je **belangrijkste config files en bestanden** upload naar **Google Drive** met `rclone`, zodat je een backup hebt.
2. Maak een **shutdown script** dat eerst alle belangrijkste bestanden upload naar **Google Drive**, en daarna aflsuit zodat je altijd een backup hebt van je meest recente bestanden.
3. Stel `Cron-jobs` in om **minstens 2 taken te automatiseren**, zoals systeem updates plannen of wekelijks downloads opruimen of organiseren.

# Systeem monitoring en processen

1. Gebruik commands zoals `top`, `htop`, of `ps` om actieve processen te bekijken.
2. Beëindig een specifiek proces veilig met `kill` of `pkill`.

# Remote connection

1. Log met een Windows-computer in op je Linux-systeem via `ssh`.
2. Kopieer bestanden van een Windows-computer naar je Linux-systeem via `SCP`.

# Servers

1. Leer hoe je een eenvoudige webserver start met `python3 -m http.server`
2. Leer hoe je een eenvoudige file-sharing server start met `python3 -m http.server 8000`.
3. Leer hoe je een lokale FTP-server opzet met `vsftpd` of `python3 -m pyftpdlib`.

{% include doelen.html data='linux-challenges' %}
