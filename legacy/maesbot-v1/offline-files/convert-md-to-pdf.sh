#!/bin/bash

# ###### #
# Checks #
# ###### #

# Check if input file is provided
if [ -z "$1" ]; then
  echo
  echo "Provide an .md file: $0 <input-markdown-file.md>"
  exit 1
fi

# Check if the file exists
input_file="$1"
if [ ! -f "$input_file" ]; then
  echo
  echo "Error: File '$input_file' not found!"
  exit 1
fi

# Check if the CSS file exists
css_file="/home/hanne/Documents/meneermaes/docs/assets/css/styles.css"
if [ ! -f "$css_file" ]; then
  echo
  echo "Error: CSS file '$css_file' not found!"
  exit 1
fi
# ########## #
# Convertion #
# ########## #

# Get the base name (filename without extension)
base_name="${input_file%.*}"

# Convert Markdown to PDF using Pandoc with optional CSS
echo
echo "Converting $input_file to PDF using pandoc..."

if [ -z "$css_file" ]; then
   pandoc "$input_file" -o "$base_name.pdf"
else
   pandoc "$input_file" --css="$css_file" -o "$base_name.pdf"
fi

if [ $? -ne 0 ]; then
   echo "Error: Failed to convert Markdown to PDF."
   exit 1
fi

echo
echo "Conversion complete! Output: $base_name.pdf"

#######################################################
# Guide

# $ bash convert-md-to-pdf.sh relative/path/to/file.md
