#!/bin/sh

# WHY I have to give my password 2 times
#    If GNOME detects you’re starting a system service (systemctl) and you’re not root, it routes that through PolicyKit (the Gnome UI).
#    Then later, sudo triggers its own password prompt for docker.
# Solutions:
#    1. Avoid starting the service manually: if Docker is already enabled on boot, you don’t need systemctl start docker
#    2. Add yourself to the docker group, so you don't need to run Docker with sudo: sudo usermod -aG docker $USER && newgrp docker

# Start docker
sudo systemctl start docker

# Build docker image
# This reads the instructions in the Dockerfile and package the application's environment, dependencies, and configurations into a reusable Docker image
# This image serves as a blueprint for containers, it is stored in the Docker daemon and can be used multiple times to start containers
sudo docker build -t maesbot .
  # This last line is the script to run when the container starts
  # . to read the Dockerfile in the current directory (.) and builds an image tagged (named) as maesbot
  # -v $(pwd):/app to mount your current directory ($(pwd)) to /app inside the container

# Run the container
sudo docker run $docker_volume_args --rm -it -v "$(pwd):/app" maesbot
   # --rm to remove the container when it exits
   # -it to create an interactive shell, can I can input stuff via fzf
   # Every time you run a Docker container without --rm, Docker keeps it in the background (even after it stops)
   # These containers accumulate over time and clutter your system.

# Fix ownership for entire project directory
sudo chown -R "$(id -u):$(id -g)" .
