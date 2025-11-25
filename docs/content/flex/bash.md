---
title: Bash
last_modified: 2025-11-25 09:22:28 +0100
created: Thu, oct 21, 2025  09:07:23 PM
---

# Bash commands

## Navigatie

| Navigatie                            | Afkorting               | Functie                                         |
|--------------------------------------|-------------------------|-------------------------------------------------|
| `pwd`                                | Print working directory | De locatie waar we zitten                       |
| `ls`                                 | List                    | Lijst met inhoud van de folder waarin we zitten |
| `ls -a`                              | List all                | Lijst met **hidden files en folders**           |
| `ls -l`                              | List in long format     | Lijst met **info**                              |
| `ls -al`                             | List all in long format | Lijst met **info & hidden files**               |
| `tree .` <br> `tree folder/folder/`  |                         | Lijst in boomstructuur                          |
| `cd folder` <br> `cd folder/folder/` | Change directory        | Naar een andere locatie gaan                    |
| `cd ..` <br> `cd ../..`              | Change directory        | Een locatie **hoger** gaan                      |
| `cd - `                              | Change directory        | Naar de **vorige** locatie gaan                 |
| `cd`                                 | Change directory        | Naar de **startlocatie** gaan                   |

## Bestanden en folders beheren

| Aanmaken          | Afkoring         | Functie                                 |
|-------------------|------------------|-----------------------------------------|
| `touch`           |                  | **Bestand** aanmaken                    |
| `mkdir`           | Make directory   | **Folder** aanmaken                     |
| `rm`              | Remove           | **Bestand** verwijderen                 |
| `rm -r`           | Remove recursive | **Folder** verwijderen                  |
| `cp file1 file2`  | Copy             | **Bestanden** kopiëren                  |
| `cp -r dir1 dir2` | Copy recursive   | **Folder** kopiëren                     |
| `mv file1 file2`  | Move             | **Bestanden** verplaatsen/**hernoemen** |
| `mv -r dir1 dir2` | Move recursive   | **Folder** verplaatsen/**hernoemen**    |
| `cat file`        | Concatenate      | Inhoud van een (tekst)file bekijken     |

## Coderen

| Coderen             | Afkoring | Functie                                            |
|---------------------|----------|----------------------------------------------------|
| `code bestand`      |          | Bestand openen in **VS Code**                      |
| `codium bestand`    |          | Bestand openen in **VS Codium**                    |
| `thonny bestand`    |          | Bestand openen in de **Raspberry Pi Code Editor**  |
| `nano bestand`      |          | Bestand openen in de **Nano Terminal Code Editor** |
| `python bestand.py` |          | Python code uitvoeren                              |

# Command line shortcuts

{% include btn.html btn='Ctrl, c' %}&#58; **Stop** het command dat aan het runnen is/**verwijder** het command dat je aan het typen bent.
{% include btn.html btn='Ctrl, a' %}&#58; Ga naar het **begin** van de lijn.
{% include btn.html btn='Ctrl, e' %}&#58; Ga naar het **einde** van de lijn.
{% include btn.html btn='Ctrl, Shift, c' %}&#58; **Copy**.
{% include btn.html btn='Ctrl, Shift, v' %}&#58; **Paste**.

`command 1 && command 2 && command 3`: Commands **chainen** *(na elkaar uitvoeren)*.

# Terminologie

{% include toggle.html title="Terminal" content="
Een **programma** waarin je tekstcommando’s kan typen.

![](images/terminal.png){: width='600px' }
" %}

{% include toggle.html title="Console" content="
Soms gebruikt men het woord console als synoniem voor terminal, maar eigenlijk verwijst een console naar de **vroegere fysieke computer** met enkel een toetsenbord en een tekstscherm, zonder grafische interface.  

![](images/console.jpg){: width='600px' }
" %}

{% include toggle.html title="Command line" content="
De **regel** waar jij je commando's typt.  
Het is niet het venster, maar de input-lijn zelf.

![](images/commandline.png){: width='600px' }
" %}

{% include toggle.html title="Shell" content="
De software die jouw commando **interpreteert en uitvoert**.  
Dat is wat er draait in de terminal.
" %}

{% include toggle.html title="Bash" content="
Bash is een **shell-taal** waarin je **commmands & scripts** kan schrijven.  
Er zijn meerdere shell-talen zoals:
- PowerShell *(op Windows)*
- Zsh *(op MacOS & Linux)*
- Bash *(op MacOS & Linux)*
- ...

![](images/shell-taal.png){: width='600px' }
" %}
