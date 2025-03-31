#!/bin/bash

# Navigate to the project directory
cd /home/hanne/Documents/meneermaes/maesbot

# Check if the container exists and is running
if [ ! "$(docker ps -q -f name=maesbot)" ]; then
  # Check if the container exists but is stopped
  if [ "$(docker ps -aq -f name=maesbot)" ]; then
    docker start maesbot
  else
    # Build and start the container
    docker-compose up -d
  fi
fi

# Run the command in the container
docker exec -it maesbot node maesbot.js
