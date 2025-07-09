#!/bin/sh

# Start docker
systemctl start docker

# Build docker image
# This reads the instructions in the Dockerfile and package the application's environment, dependencies, and configurations into a reusable Docker image
# This image serves as a blueprint for containers, it is stored in the Docker daemon and can be used multiple times to start containers
sudo docker run \
  -v $(pwd):/app \
  maesbot \
  python taken-en-toetsen/1-yaml2doc.py
  # This last line is the script to run when the container starts
  # . to read the Dockerfile in the current directory (.) and builds an image tagged (named) as maesbot
  # -v $(pwd):/app to mount your current directory ($(pwd)) to /app inside the container

# Run the container
docker run --rm maesbot
   # --rm to remove the container when it exits
   # Every time you run a Docker container without --rm, Docker keeps it in the background (even after it stops)
   # These containers accumulate over time and clutter your system.
