# Use a base image with Node.js
FROM node:18

# Install Python, fzf, and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    bash \
    git \
    curl \
    && curl -L https://github.com/junegunn/fzf/releases/download/0.35.1/fzf-0.35.1-linux_amd64.tar.gz | tar xzC /usr/local/bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy package.json files first (for better caching)
COPY punten/package*.json ./punten/

# Install Node.js dependencies
WORKDIR /app/punten
RUN npm install
WORKDIR /app

# Copy the rest of your application
COPY . .

# Make scripts executable
RUN chmod +x /app/offline-files/convert-md-to-pdf.sh /app/punten/sheet-to-doc.sh

# Command to run when container starts
ENTRYPOINT ["node", "maesbot.js"]
