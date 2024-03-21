#!/bin/bash

# Define the directory
directory="docs/content"

# Function to list files recursively with indentation
list_files() {
    local path="$1"
    local indent="$2"

    # List files and directories in the current path
    for entry in "$path"/*; do
        # Get basename of the entry
        local basename="$(basename "$entry")"
        
        # Check if the entry is a directory or file
        if [ -d "$entry" ]; then
            # Print directory name with yellow color, '/' after the name, and appropriate indentation
            echo -e "${indent}\033[33m$basename/\033[0m"
            # If the entry is a directory, recursively list its contents with increased indentation
            list_files "$entry" "$indent\t"
        else
            # Print file name with cyan color and appropriate indentation
            echo -e "${indent}\033[36m$basename\033[0m"
        fi
    done
}

# Start listing files recursively from the specified directory
list_files "$directory" ""
