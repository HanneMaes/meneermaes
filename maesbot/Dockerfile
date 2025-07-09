# Debian-based image with:
FROM debian:bullseye

# Install Python, pip, and LibreOffice
RUN apt-get update && \
    apt-get install -y \
    python3 python3-pip \
    libreoffice \
    unzip make bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR /app

# Copy and install dependencies
COPY requirements-python.txt .
RUN pip3 install --no-cache-dir -r requirements-python.txt

# Copy project files
COPY . .

# Run script
CMD ["python3", "taken-en-toetsen/1-yaml2doc.py"]
