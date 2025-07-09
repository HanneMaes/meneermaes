# Debian-based image with:
#   - Python 3.11 preinstalled
#   - bash, apt, and common CLI tools
# A good base for running LibreOffice, PDF conversion, file copying, etc.
FROM python:3.11-bullseye

# Set environment vars to allow headless LibreOffice
ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/root

# Install needed tools: bash, LibreOffice (for .odt -> .pdf), etc.
RUN apt-get update && \
    apt-get install -y \
    bash \
    libreoffice \
    unzip \
    make \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements-python.txt .
RUN pip install --no-cache-dir -r requirements-python.txt

# Copy the rest of the project
COPY . .
