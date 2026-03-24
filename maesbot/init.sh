#!/bin/bash
# init.sh - Smart Docker Compose wrapper
# This script:
# 1. Checks if Docker is running (starts it if needed)
# 2. Checks if docker-compose.yml exists
# 3. Builds image if needed
# 4. Runs your application using Docker Compose

set -e # Exit on any error

# Colors for output
NC='\033[0m' # No Color
CYAN='\033[0;36m'
BRIGHT_CYAN='\033[1;36m'
GREEN='\033[0;32m'
BRIGHT_GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
DARK_GREY='\033[0;90m'
GREY='\033[0;37m'
BOLD='\033[1m'
UNDERLINE='\033[4m'
ITALIC='\033[3m'

# Print everything in grey
echo -e "${DARK_GREY}"

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
  echo -e "${RED}✗ Error: docker-compose.yml not found!${DARK_GREY}"
  echo ""
  echo "Please create docker-compose.yml in the current directory."
  exit 1
fi

# Check if Docker is running, start if needed
echo "Checking Docker..."

# Check if we need sudo for docker commands
DOCKER_CMD="docker"
COMPOSE_CMD="docker compose"

if ! docker info >/dev/null 2>&1; then
  # Try with sudo
  if sudo docker info >/dev/null 2>&1; then
    DOCKER_CMD="sudo docker"
    COMPOSE_CMD="sudo docker compose"
    echo "Using sudo for Docker (run 'newgrp docker' or log out/in to fix)"
  fi
fi

# Now check if Docker is actually running
if ! $DOCKER_CMD info >/dev/null 2>&1; then
  echo "Docker daemon is not running"
  echo "Attempting to start Docker..."
  echo ""

  # Try to start Docker with systemctl
  if sudo systemctl start docker 2>/dev/null; then
    sleep 3 # Wait for Docker to fully start

    # Check again
    if $DOCKER_CMD info >/dev/null 2>&1; then
      echo "Docker started successfully"
    else
      echo -e "${RED}✗ Docker service started but daemon not responding${DARK_GREY}"
      echo ""
      echo "Troubleshooting steps:"
      echo "  1. Check status: sudo systemctl status docker"
      echo "  2. Check logs: sudo journalctl -u docker -n 50"
      echo "  3. Try manual start: sudo systemctl start docker"
      exit 1
    fi
  else
    echo "systemctl failed, trying alternative methods..." # systemctl failed, try alternative methods

    # Try with snap
    if command -v snap >/dev/null 2>&1; then
      if sudo snap start docker 2>/dev/null; then
        sleep 3
        if $DOCKER_CMD info >/dev/null 2>&1; then
          echo "Docker started via snap"
        fi
      fi
    fi

    # Final check
    if ! $DOCKER_CMD info >/dev/null 2>&1; then
      echo -e "${RED}✗ Failed to start Docker${DARK_GREY}"
      echo ""
      echo "Please diagnose and start Docker manually:"
      echo "  sudo systemctl status docker    # Check service status"
      echo "  sudo systemctl start docker     # Start with systemctl"
      echo "  sudo journalctl -u docker -n 50 # Check logs"
      echo ""
      echo "Or if using snap:"
      echo "  sudo snap start docker"
      exit 1
    fi
  fi
else
  echo "Docker is running"
fi

# ###########################################################################
# Check if we need to build

echo "Checking if build is needed..."

NEEDS_BUILD=false

# Check if image exists
if ! $DOCKER_CMD image inspect maesbot:latest >/dev/null 2>&1; then
  echo "Image doesn't exist"
  NEEDS_BUILD=true
else
  # Get image creation time
  IMAGE_TIME=$($DOCKER_CMD image inspect -f '{{.Created}}' maesbot:latest)
  IMAGE_TIMESTAMP=$(date -d "$IMAGE_TIME" +%s 2>/dev/null || echo 0)

  # Check if Dockerfile changed
  if [ -f "Dockerfile" ]; then
    DOCKERFILE_TIMESTAMP=$(stat -c %Y Dockerfile 2>/dev/null || stat -f %m Dockerfile 2>/dev/null || echo 0)
    if [ "$DOCKERFILE_TIMESTAMP" -gt "$IMAGE_TIMESTAMP" ]; then
      echo -e "${NC}Dockerfile changed${DARK_GREY}"
      NEEDS_BUILD=true
    fi
  fi

  # Check if requirements.txt changed
  if [ -f "requirements.txt" ]; then
    REQ_TIMESTAMP=$(stat -c %Y requirements.txt 2>/dev/null || stat -f %m requirements.txt 2>/dev/null || echo 0)
    if [ "$REQ_TIMESTAMP" -gt "$IMAGE_TIMESTAMP" ]; then
      echo -e "${NC}requirements.txt changed${DARK_GREY}"
      NEEDS_BUILD=true
    fi
  fi

  if [ "$NEEDS_BUILD" = false ]; then
    echo "Image is up to date"
  fi
fi

# ###########################################################################
# Build if needed

if [ "$NEEDS_BUILD" = true ]; then
  echo -e "${NC}Building image..."
  echo ""
  $COMPOSE_CMD build
  echo ""
  echo -e "${NC}Build complete"
fi

# ###########################################################################
# Run the application

echo -e "${DARK_GREY}Starting MAESBOT"
echo ""

# ###########################################################################
# Open a folder if needed

# Run the container and capture the output folder path
mkdir -p /tmp/maesbot_output_dir
chmod 777 /tmp/maesbot_output_dir

$COMPOSE_CMD run --rm maesbot

FOLDER_PATH=$(cat /tmp/maesbot_output_dir/folder 2>/dev/null)
rm -f /tmp/maesbot_output_dir/folder

# Convert container path to host path
FOLDER_PATH="${FOLDER_PATH/\/data\/input\//\/home\/hanne\/Documents\/meneermaes\/docs\/_data\/}"
FOLDER_PATH="${FOLDER_PATH/\/data\/private\//\/home\/hanne\/Documents\/Nextcloud\/School\/Automatisatie\/maesbot-private-data\/}"

# Open the folder if a path was returned
if [ -n "$FOLDER_PATH" ]; then
  echo -e "\n${DARK_GREY}Opening: ${FOLDER_PATH}${NC}"
  if command -v wslview >/dev/null 2>&1; then
    WIN_PATH=$(wslpath -w "$FOLDER_PATH")
    wslview "$WIN_PATH" 2>/dev/null &
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$FOLDER_PATH" 2>/dev/null &
  elif command -v open >/dev/null 2>&1; then
    open "$FOLDER_PATH" 2>/dev/null &
  else
    echo -e "${RED}✗ Could not auto-open folder${NC}"
    echo -e "${RED}Path: ${FOLDER_PATH}${NC}"
  fi
fi
