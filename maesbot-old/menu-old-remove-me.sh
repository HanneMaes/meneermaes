#!/bin/bash

############################################################################################################
# Menu items
declare -A scripts

scripts["1.1 Create sheets"]="Punten/1-data2sheet.py"
scripts["1.2 Sheets to PDF"]="Punten/2-sheet2pdf.sh"

############################################################################################################

cd "$(dirname "$0")"

# Load config variables from settings.conf
source settings.conf
echo ""
echo "settings.conf -> private_data_dir: $private_data_dir"
echo "settings.conf -> punten_dir: $punten_dir"
echo ""

# Get the list of menu items (keys of the array)
menu_items=("${!scripts[@]}")

# Use fzf to select a menu item
selected=$(printf '%s\n' "${menu_items[@]}" | fzf --prompt="Select script: ")
script="${scripts[$selected]}"

# Exit if nothing selected
if [[ -z "$selected" ]]; then
    echo "No selection made"
    exit 1
fi

############################################################################################################
# Execute selected menu item

if [[ "$script" == "Punten/1-data2sheet.py" ]]; then

    echo "script: $script"

    # Find yaml files in punten_dir and select one via fzf
    selected_file=$(find "$punten_dir" -type f -name '*.yml' | fzf --prompt="Select YAML file: ")
    echo "selected_file: $selected_file"
    if [[ -z "$selected_file" ]]; then
      echo "No YAML file selected"
      exit 1
    fi

    # Call python script with selected file path and output dir
    # python3 "$script" --input "$selected_file" --output "$private_data_dir/Punten/Output"

fi
