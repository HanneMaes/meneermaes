---
title: Bash Basics
last_modified: 2026-11-24 15:21:23 +0100
created: Thu, oct 21, 2025  09:07:23 PM
---

# Bash basic commands

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

## Help command

Met het argument `--help` kan je bij veel Bash-commando's een overzicht opvragen van de beschikbare opties en hun werking.

Bijvoorbeeld, het command `cd --help` geeft dit:
```bash 
cd: cd [-L|[-P [-e]]] [-@] [dir]
    Change the shell working directory.

    Change the current directory to DIR.  The default DIR is the value of the
    HOME shell variable. If DIR is "-", it is converted to $OLDPWD.

    The variable CDPATH defines the search path for the directory containing
    DIR.  Alternative directory names in CDPATH are separated by a colon (:).
    A null directory name is the same as the current directory.  If DIR begins
    with a slash (/), then CDPATH is not used.

    If the directory is not found, and the shell option `cdable_vars' is set,
    the word is assumed to be  a variable name.  If that variable has a value,
    its value is used for DIR.

    Options:
      -L        force symbolic links to be followed: resolve symbolic
                links in DIR after processing instances of `..'
      -P        use the physical directory structure without following
                symbolic links: resolve symbolic links in DIR before
                processing instances of `..'
      -e        if the -P option is supplied, and the current working
                directory cannot be determined successfully, exit with
                a non-zero status
      -@        on systems that support it, present a file with extended
                attributes as a directory containing the file attributes

    The default is to follow symbolic links, as if `-L' were specified.
    `..' is processed by removing the immediately previous pathname component
    back to a slash or the beginning of DIR.

    Exit Status:
    Returns 0 if the directory is changed, and if $PWD is set successfully when
    -P is used; non-zero otherwise
```

# Command line shortcuts

- {% include btn.html btn='Ctrl, c' %}&#58; **Stop** het command dat aan het runnen is/**verwijder** het command dat je aan het typen bent.
- {% include btn.html btn='Ctrl, a' %}&#58; Ga naar het **begin** van de lijn.
- {% include btn.html btn='Ctrl, e' %}&#58; Ga naar het **einde** van de lijn.
- {% include btn.html btn='Ctrl, Shift, c' %}&#58; **Copy**.
- {% include btn.html btn='Ctrl, Shift, v' %}&#58; **Paste**.
- `command 1 && command 2 && command 3`: Commands **chainen** *(na elkaar uitvoeren)*.

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
Bash is een **shell-taal** waarin je **commands & scripts** kan schrijven.  
Er zijn meerdere shell-talen zoals:
- PowerShell *(op Windows)*
- Zsh *(op MacOS & Linux)*
- Bash *(op MacOS & Linux)*
- ...

![](images/shell-taal.png){: width='600px' }
" %}

# Games om bash te leren

{% include cursusmateriaal/bash-games.md %}
