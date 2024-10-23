#!/bin/sh

# Start docker
systemctl start docker

# Build docker image
# This reads the instructions in the Dockerfile and package the application's environment, dependencies, and configurations into a reusable Docker image
# This image serves as a blueprint for containers, it is stored in the Docker daemon and can be used multiple times to start containers
sudo docker build -t meneermaes-jekyll .
   # Read the Dockerfile in the current directory (.) and builds an image tagged as meneermaes-jekyll

# Run the Docker container with LiveReload enabled
# Creates and starts a new container for a specific image
# Runs any default commands specified in the image’s CMD or ENTRYPOINT
sudo docker run \
    -p 4000:4000 \
    -p 35729:35729 \
    -v $(pwd):/app \
    meneermaes-jekyll \
    bundle exec jekyll serve \
    --livereload \
    --force_polling \
    --host 0.0.0.0 \
    & # Run in background

# Wait a few seconds for Jekyll to start
sleep 5

# Open website in Firefox
firefox http://127.0.0.1:4000/
