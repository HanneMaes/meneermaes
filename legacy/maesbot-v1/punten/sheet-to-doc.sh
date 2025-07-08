#!/bin/bash

sheet="/home/hanne/Documents/Nextcloud/School/maesbot-private-data/Punten/adam.xlsx"
output_dir="/home/hanne/Documents/Nextcloud/School/maesbot-private-data/Punten/"

# Ensure the output directory exists
mkdir -p "$output_dir"

# Convert the Excel sheet to text and specify the output directory
libreoffice --headless --convert-to txt:"Text - txt - csv (StarCalc)" --outdir "$output_dir" "$sheet"
