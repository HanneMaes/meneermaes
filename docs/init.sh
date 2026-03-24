#!/bin/sh

# Start docker (works on both WSL and native NixOS)
if command -v systemctl &> /dev/null && systemctl is-system-running &> /dev/null 2>&1; then
    sudo systemctl start docker
fi

# Build docker image
# This reads the instructions in the Dockerfile and package the application's environment, dependencies, and configurations into a reusable Docker image
# This image serves as a blueprint for containers, it is stored in the Docker daemon and can be used multiple times to start containers
sudo docker build -t meneermaes-jekyll .
# Read the Dockerfile in the current directory (.) and builds an image tagged (named) as meneermaes-jekyll

# Run the Docker container with LiveReload enabled
# Creates and starts a new container for a specific image
# Runs any default commands specified in the image’s CMD or ENTRYPOINT
sudo docker run \
    --rm \
    -p 4000:4000 \
    -p 35729:35729 \
    -v $(pwd):/app \
    meneermaes-jekyll \
    bundle exec jekyll serve \
    --livereload \
    --force_polling \
    --host 0.0.0.0 \
    & # Run in background
    # --rm to remove the container when it exits
    # Every time you run a Docker container without --rm, Docker keeps it in the background (even after it stops)
    # These containers accumulate over time and clutter your system.

# Wait for Jekyll to be ready
echo "Waiting for Jekyll..."
until curl -s http://127.0.0.1:4000/ > /dev/null; do
    sleep 1
done 

# Open website in default browser
if command -v wslview &> /dev/null; then
    wslview http://127.0.0.1:4000/ # WSL
else
    xdg-open http://127.0.0.1:4000/ # Pure Linux
fi
