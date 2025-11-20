#!/usr/bin/env bash

# Create dirs
mkdir -p bash-toets/.config/hidden
mkdir -p bash-toets/docs/extra
mkdir -p bash-toets/projecten/alpha/data/verborgen
mkdir -p bash-toets/projecten/alpha/scripts
mkdir -p bash-toets/projecten/beta/analyse/debug-info
mkdir -p bash-toets/scripts

# Config
echo "TOKEN=XYZ123" >bash-toets/.config/hidden/.token
echo "SESSION_KEY=ABC456" >bash-toets/.config/hidden/.session_key
echo "theme=dark" >bash-toets/.config/settings.conf

# Docs
echo "Handleiding voor gebruikers" >"bash-toets/docs/handleiding gebruiker.txt"
echo "Wijzigingen versie 1.2" >bash-toets/docs/changelog-v1.2.txt
echo "Foutanalyse rapport" >"bash-toets/docs/extra/fout analyse 2024.md"
echo "Tip 1: Gebruik de terminal" >"bash-toets/docs/extra/tips & tricks.txt"

# Project alpha
echo "Project Alpha Readme" >bash-toets/projecten/alpha/README.md
echo -e "1\n2\n3\n4\n5\n6\n7\n8\n9\n10" >bash-toets/projecten/alpha/data/cijfers_1.txt
echo -e "11\n12\n13\n14" >bash-toets/projecten/alpha/data/cijfers_2.txt
echo "GEHEIME_SLEUTEL" >bash-toets/projecten/alpha/data/verborgen/.sleutel
echo "Sleutel" >bash-toets/projecten/alpha/data/verborgen/sleutel

echo -e "#!/bin/bash\necho Running start" >bash-toets/projecten/alpha/scripts/start.sh
echo -e "print('GELUKT!')" >"bash-toets/projecten/alpha/scripts/run dit script.py"

# Project beta
echo "Eindverslag" >"bash-toets/projecten/beta/verslag eindversie.txt"
echo "LOG: alles ok" >bash-toets/projecten/beta/analyse/log_01.log
echo "LOG: error gevonden" >bash-toets/projecten/beta/analyse/log_02.log
echo "Probleem A details" >"bash-toets/projecten/beta/analyse/debug-info/probleem A.txt"
echo "Analyse B final" >"bash-toets/projecten/beta/analyse/debug-info/analyse B (final).txt"

# Scripts root
echo -e "#!/bin/bash\necho 'Open mij script uitgevoerd!'" >"bash-toets/scripts/open mij.sh"

# FINISHED
echo
echo "Veel succes met de toets!"
