#!/bin/bash

# bash new.sh <page/punt> dir/file (with our without extension)

#####################################################################################################################

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
    echo "$(echo "$2" | awk '{for(i=1;i<=NF;i++){$i=toupper(substr($i,1,1)) tolower(substr($i,2));}; print}')"
}

#####################################################################################################################
# script
#####################################################################################################################

# Where to put the files
rootdir=""
content=""
extension=""

# Remove filename from extension
filename=$(basename -- "$2")
filename_no_extension="${filename%.*}"
filename_no_extension_capitalized=$(capitalize_dir "$filename_no_extension")

########
# PAGE #
########

if [[ "$1" == "page" ]]; then

    # Where to put the files
    rootdir="content"

    # Create directory if it doesn't exist
    directory=$(dirname -- "$2")
    mkdir -p "$rootdir/$directory"

    # Define the content
    content="---
    title: $filename_no_extension_capitalized
    date: $(date +'%Y-%m-%d %H:%M:%S %z')
    ---"

    # If the filename does not end with ".md", add it
    if [[ $2 != *.md ]]; then
        extension=".md"
    fi

########
# PUNT #
########

elif [[ "$1" == "another_value" ]]; then

    # Where to put the files
    rootdir="_data"

    # Define the content
    content="onderdeel, punt"

    # If the filename does not end with ".csv", add it
    if [[ $2 != *.csv ]]; then
        extension=".csv"
    fi

###############
# CREATE RILE #
###############
fi

# Create the file with the content
echo "$content" > "$rootdir/$2$extension"

echo ""
echo -e "File ${color1}'$rootdir/$2$extension'${nocolor} created with the following content:"
echo ""
echo -e "${color2}$content"

# Open the file
code "$rootdir/$2$extension"