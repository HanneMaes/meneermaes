#!/bin/bash

URL="https://www.meneermaes.be/"

# Get the hostname from the URL (e.g. your-site.github.io)
HOSTNAME=$(echo "$URL" | awk -F/ '{print $3}')

# Get current date in YY-MM-DD format
DATESTAMP=$(date +%y-%m-%d)

# Combine for folder name
FOLDER="offline-website/${DATESTAMP}_${HOSTNAME}"

# Create folder and download the website into it
mkdir -p "$FOLDER" && \
cd "$FOLDER" && \
wget \
  --mirror \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-parent \
  "$URL"

# Finished
echo ""
echo "✅ Website downloaded to: $FOLDER"

###################################################""
# Guide

# Creates a folder 'offline-website/date_www.meneermaes.be
# Donwloads the live meneermaes.be to this folder, the website fully works offline

# bash offline-website-downloader.sh
