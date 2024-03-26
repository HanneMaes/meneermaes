#!/bin/bash

# Black        0;30     Dark Gray     1;30
# Red          0;31     Light Red     1;31
# Green        0;32     Light Green   1;32
# Brown/Orange 0;33     Yellow        1;33
# Blue         0;34     Light Blue    1;34
# Purple       0;35     Light Purple  1;35
# Cyan         0;36     Light Cyan    1;36
# Light Gray   0;37     White         1;37

# color settings
nocolor='\033[0m'
color1='\033[0;35m'
color2='\033[0;36m'

#####################################################################################################################

# Function to capitalize directory names
capitalize_dir() {
    echo "$(echo "$1" | awk '{for(i=1;i<=NF;i++){$i=toupper(substr($i,1,1)) tolower(substr($i,2));}; print}')"
}

#####################################################################################################################
# script
#####################################################################################################################

# Check if a file path is provided as an argument
if [ $# -ne 1 ]; then
    echo "Please provide a file path: $0 <file_path/file>"
    exit 1
fi

# Where to put the files
rootdir="content"

# Extract filename without extension
filename=$(basename -- "$1")
filename_no_extension="${filename%.*}"
filename_no_extension_capitalized=$(capitalize_dir "$filename_no_extension")

# Create directory if it doesn't exist
directory=$(dirname -- "$1")
mkdir -p "$rootdir/$directory"

# Define the content
content="---
title: $filename_no_extension_capitalized
date: $(date)
---"

# If the filename does not end with ".md", add it
extension=""
if [[ $1 != *.md ]]; then
    extension=".md"
fi

# Create the file with the content
echo "$content" > "$rootdir/$1$extension"

echo ""
echo -e "File ${color1}'$rootdir/$1$extension'${nocolor} created with the following content:"
echo ""
echo -e "${color2}$content"

# Open the file
code "$rootdir/$1$extension"