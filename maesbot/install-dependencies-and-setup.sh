#!/bin/bash

# ============================================================================
# setup.sh - Complete setup for maesbot
# ============================================================================
# This script:
# 1. Checks if Docker is installed and running
# 2. Creates all necessary files if missing
# 3. Builds the Docker image
# 4. Runs a test
# ============================================================================

set -e # Exit on any error

echo "🤖 MaesBot Setup Script"
echo "======================"
echo ""

# ============================================================================
# Check Docker installation
# ============================================================================
echo "📋 Checking Docker installation..."

if ! command -v docker &>/dev/null; then
  echo "❌ Docker is not installed!"
  echo ""
  echo "Install Docker with:"
  echo "  sudo apt update"
  echo "  sudo apt install docker.io"
  echo "  sudo systemctl start docker"
  echo "  sudo usermod -aG docker $USER"
  echo ""
  echo "After adding yourself to docker group, log out and back in."
  exit 1
fi

echo "✅ Docker is installed"

# ============================================================================
# Check if Docker daemon is running
# ============================================================================
echo "📋 Checking Docker daemon..."

if ! docker info >/dev/null 2>&1; then
  echo "⚠️  Docker daemon is not running"
  echo "Starting Docker..."

  sudo systemctl start docker

  # Wait a bit for Docker to start
  sleep 2

  if ! docker info >/dev/null 2>&1; then
    echo "❌ Failed to start Docker daemon"
    echo "Try manually: sudo systemctl start docker"
    exit 1
  fi
fi

echo "✅ Docker daemon is running"
echo ""

# ============================================================================
# Check required files
# ============================================================================
echo "📋 Checking required files..."

MISSING_FILES=()

if [ ! -f "Dockerfile" ]; then
  MISSING_FILES+=("Dockerfile")
fi

if [ ! -f "requirements.txt" ]; then
  MISSING_FILES+=("requirements.txt")
fi

if [ ! -f "fuzzypicker.py" ]; then
  MISSING_FILES+=("fuzzypicker.py")
fi

if [ ! -f "main.py" ]; then
  MISSING_FILES+=("main.py")
fi

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
  echo "❌ Missing required files:"
  for file in "${MISSING_FILES[@]}"; do
    echo "   - $file"
  done
  echo ""
  echo "Please create these files first!"
  exit 1
fi

echo "✅ All required files present"
echo ""

# ============================================================================
# Make scripts executable
# ============================================================================
echo "📋 Making scripts executable..."

chmod +x build.sh 2>/dev/null || true
chmod +x run.sh 2>/dev/null || true
chmod +x setup.sh 2>/dev/null || true

echo "✅ Scripts are executable"
echo ""

# ============================================================================
# Build Docker image
# ============================================================================
echo "🔨 Building Docker image..."
echo ""

./build.sh

echo ""

# ============================================================================
# Success message
# ============================================================================
echo "✅ Setup complete!"
echo ""
echo "Available commands:"
echo "  ./run.sh              - Start interactive shell"
echo "  ./run.sh python main.py - Run main.py"
echo "  ./build.sh            - Rebuild image"
echo ""
echo "Try it now:"
echo "  ./run.sh python main.py"
echo ""
