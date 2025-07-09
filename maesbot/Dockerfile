# Debian-based image with:
FROM python:3.11-slim

# Install Bash, make, etc.
RUN apt-get update && apt-get install -y \
    bash \
    make \
    unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
COPY requirements-python.txt .
RUN pip install --no-cache-dir -r requirements-python.txt

# Default command
CMD ["python", "taken-en-toetsen/1-yaml2doc.py"]
