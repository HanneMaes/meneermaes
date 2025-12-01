#!/bin/bash
# ============================================================================
# start.sh - Smart build and run script
# ============================================================================
# This script:
# 1. Checks if Docker is running
# 2. Checks if image needs rebuilding (Dockerfile or requirements.txt changed)
# 3. Rebuilds only if necessary
# 4. Runs your application
# ============================================================================

set -e # Exit on any error

IMAGE_NAME="maesbot:latest"
BUILD_CONTEXT="."

# ============================================================================
# Colors for output
# ============================================================================
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# Check if Docker is running, start if needed
# ============================================================================
echo "Checking Docker..."

# Check if we need sudo for docker commands
DOCKER_CMD="docker"
if ! docker info >/dev/null 2>&1; then
  # Try with sudo
  if sudo docker info >/dev/null 2>&1; then
    DOCKER_CMD="sudo docker"
    echo " Using sudo for Docker (run 'newgrp docker' or log out/in to fix)"
  fi
fi

# Now check if Docker is actually running
if ! $DOCKER_CMD info >/dev/null 2>&1; then
  echo " Docker daemon is not running"
  echo "Attempting to start Docker..."
  echo ""

  # Try to start Docker with systemctl
  if sudo systemctl start docker 2>/dev/null; then
    # Wait a moment for Docker to fully start
    sleep 3

    # Check again
    if $DOCKER_CMD info >/dev/null 2>&1; then
      echo "Docker started successfully"
    else
      echo -e "${RED}❌ Docker service started but daemon not responding${NC}"
      echo ""
      echo "Troubleshooting steps:"
      echo "  1. Check status: sudo systemctl status docker"
      echo "  2. Check logs: sudo journalctl -u docker -n 50"
      echo "  3. Try manual start: sudo systemctl start docker"
      exit 1
    fi
  else
    # systemctl failed, try alternative methods
    echo "systemctl failed, trying alternative methods..."

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
      echo -e "${RED}❌ Failed to start Docker${NC}"
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

# ============================================================================
# Check if rebuild is needed
# ============================================================================
NEEDS_BUILD=false

# Check if image exists
if ! $DOCKER_CMD image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
  echo "Image doesn't exist, building..."
  NEEDS_BUILD=true
else
  # Get image creation time
  IMAGE_TIME=$($DOCKER_CMD image inspect -f '{{.Created}}' "$IMAGE_NAME")
  IMAGE_TIMESTAMP=$(date -d "$IMAGE_TIME" +%s 2>/dev/null || echo 0)

  # Check if Dockerfile is newer than image
  if [ -f "Dockerfile" ]; then
    DOCKERFILE_TIMESTAMP=$(stat -c %Y Dockerfile 2>/dev/null || stat -f %m Dockerfile 2>/dev/null || echo 0)
    if [ "$DOCKERFILE_TIMESTAMP" -gt "$IMAGE_TIMESTAMP" ]; then
      echo "Dockerfile changed, rebuilding..."
      NEEDS_BUILD=true
    fi
  fi

  # Check if requirements.txt is newer than image
  if [ -f "requirements.txt" ]; then
    REQ_TIMESTAMP=$(stat -c %Y requirements.txt 2>/dev/null || stat -f %m requirements.txt 2>/dev/null || echo 0)
    if [ "$REQ_TIMESTAMP" -gt "$IMAGE_TIMESTAMP" ]; then
      echo "  requirements.txt changed, rebuilding..."
      NEEDS_BUILD=true
    fi
  fi

  if [ "$NEEDS_BUILD" = false ]; then
    echo "Image is up to date"
  fi
fi

# ============================================================================
# Build if needed
# ============================================================================
if [ "$NEEDS_BUILD" = true ]; then
  echo ""
  echo "Building image..."
  $DOCKER_CMD build -t "$IMAGE_NAME" "$BUILD_CONTEXT"
  echo "Build complete"
fi

# ============================================================================
# Run the application
# ============================================================================
echo "Starting application..."
echo ""

# Run with arguments if provided, otherwise run main.py
if [ $# -eq 0 ]; then
  # Default: run main.py
  $DOCKER_CMD run -it --rm \
    -v "$(pwd):/app" \
    -w /app \
    "$IMAGE_NAME" \
    python main.py
else
  # Run with custom arguments
  $DOCKER_CMD run -it --rm \
    -v "$(pwd):/app" \
    -w /app \
    "$IMAGE_NAME" \
    "$@"
fi
